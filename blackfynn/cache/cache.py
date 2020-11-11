from __future__ import absolute_import, division, print_function
from builtins import filter, object, zip

import io
import multiprocessing as mp
import os
import platform
import sqlite3
import time
from datetime import datetime
from glob import glob
from itertools import groupby

from blackfynn import log
from blackfynn.extensions import numpy as np
from blackfynn.extensions import pandas as pd
from blackfynn.extensions import require_extension
from blackfynn.models import DataPackage, TimeSeriesChannel
from blackfynn.utils import usecs_since_epoch, usecs_to_datetime

from .cache_segment_pb2 import CacheSegment

logger = log.get_logger("blackfynn.cache")


def filter_id(some_id):
    return some_id.replace(":", "_").replace("-", "_")


def remove_old_pages(cache, mbdiff):
    # taste the rainbow!
    n = int(1.5 * ((mbdiff * 1024 * 1024) / 100) / cache.page_size) + 5

    # 2. Delete some pages from cache
    with cache.index_con as con:
        logger.debug("Cache - removing {} pages...".format(n))
        # find the oldest/least accessed pages
        q = """
            SELECT channel,page,access_count,last_access
            FROM ts_pages
            ORDER BY last_access ASC, access_count ASC
            LIMIT {num_pages}
        """.format(
            num_pages=n
        )
        pages = con.execute(q).fetchall()

    # remove the selected pages
    pages_by_channel = groupby(pages, lambda x: x[0])
    for channel, page_group in pages_by_channel:
        _, pages, counts, times = list(zip(*page_group))
        # remove page files
        cache.remove_pages(channel, *pages)

    with cache.index_con as con:
        con.execute("VACUUM")

    logger.debug("Cache - {} pages removed.".format(n))
    return n


def compact_cache(cache, max_mb):
    logger.debug("Inspecting cache...")
    wait = 2
    current_mb = cache.size / (1024.0 * 1024)
    desired_mb = 0.9 * max_mb
    while current_mb > desired_mb:
        logger.debug(
            "Cache - current: {:02f} MB, maximum: {} MB".format(current_mb, max_mb)
        )
        try:
            remove_old_pages(cache, current_mb - desired_mb)
        except sqlite3.OperationalError:
            logger.debug(
                "Cache - Index DB was locked, waiting {} seconds...".format(wait)
            )
            if wait >= 1024:
                logger.error("Cache - Unable to compact cache!")
                return  # silently fail
            time.sleep(wait)
            wait = wait * 2
        current_mb = cache.size / (1024.0 * 1024)


@require_extension
def create_segment(channel, series):
    segment = CacheSegment()
    segment.channelId = channel.id
    segment.index = series.index.astype(np.int64).values.tobytes()
    segment.data = series.values.tobytes()
    return segment


@require_extension
def read_segment(channel, bytes):
    segment = CacheSegment.FromString(bytes)
    index = pd.to_datetime(np.frombuffer(segment.index, np.int64))
    data = np.frombuffer(segment.data, np.double)
    series = pd.Series(data=data, index=index, name=channel.name)
    return series


class Cache(object):
    def __init__(self, settings):
        self._conn = None
        self.dir = settings.cache_dir
        self.index_loc = settings.cache_index
        self.write_counter = 0

        # this might be replaced with existing page size (from DB)
        self.page_size = settings.ts_page_size

        self.settings = settings
        self.init_dir()

    @property
    def index_con(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.index_loc, timeout=60)
        return self._conn

    def init_dir(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            os.chmod(self.dir, 0o775)
        index_dir = os.path.dirname(self.index_loc)
        if not os.path.exists(index_dir):
            os.makedirs(self.index_loc)
            os.chmod(self.index_loc, 0o775)

    def init_tables(self):
        with self.index_con as con:
            self.init_index_table(con)
            self.init_settings_table(con)

    def init_index_table(self, con):
        # check for index table
        q = "SELECT name FROM sqlite_master WHERE type='table' AND name='ts_pages'"
        r = con.execute(q)
        if r.fetchone() is None:
            logger.info("Cache - Creating 'ts_pages' table")
            # create index table
            q = """
                CREATE TABLE ts_pages (
                    channel CHAR(50) NOT NULL,
                    page INTEGER NOT NULL,
                    access_count INTEGER NOT NULL,
                    last_access DATETIME NOT NULL,
                    has_data BOOLEAN,
                    PRIMARY KEY (channel, page))
            """
            con.execute(q)

    def init_settings_table(self, con):
        # check for settings table
        q = "SELECT name FROM sqlite_master WHERE type='table' AND name='settings'"
        r = con.execute(q)
        if r.fetchone() is None:
            logger.info("Cache - Creating 'settings' table")
            # create settings table
            q = """
                CREATE TABLE settings (
                    ts_page_size INTEGER NOT NULL,
                    ts_format    CHAR(50) NOT NULL,
                    max_bytes    INTEGER NOT NULL,
                    modified     DATETIME)
            """
            con.execute(q)

            # insert settings values
            q = """
                INSERT INTO settings
                VALUES ({page_size}, '{format}', {max_bytes},'{time}')
            """.format(
                page_size=self.page_size,
                format="PROTOBUF",
                max_bytes=self.settings.cache_max_size,
                time=datetime.now().isoformat(),
            )
            con.execute(q)

        else:
            # settings table exists

            # 1. check for ts_format field (not there indicating old cache)
            result = con.execute("PRAGMA table_info('settings');").fetchall()
            fields = list(zip(*result))[1]
            if "ts_format" not in fields:
                # this means they used an older client to initalize the cache, and because
                # we switched the serialization format, we'll need to refresh it.
                logger.warn(
                    "Deprecated cache format detected - clearing & reinitializing cache..."
                )
                self.clear()

            # 2. check page size
            result = con.execute("SELECT ts_page_size FROM settings").fetchone()
            if result is not None:
                #  page size entry exists
                self.page_size = result[0]
                if self.settings.ts_page_size != self.page_size:
                    logger.warn(
                        "Using existing page_size={} from DB settings (user specified page_size={})".format(
                            self.page_size, self.settings.ts_page_size
                        )
                    )
            else:
                # somehow, there is no page size entry
                self.page_size = self.settings.ts_page_size

    def set_page(self, channel, page, has_data):
        with self.index_con as con:
            q = "INSERT INTO ts_pages VALUES ('{channel}',{page},0,'{time}',{has_data})".format(
                channel=channel.id,
                page=page,
                time=datetime.now().isoformat(),
                has_data=int(has_data),
            )
            con.execute(q)

    def set_page_data(self, channel, page, data, update=False):
        has_data = False if data is None else len(data) > 0
        if has_data:
            # there is data, write it to file
            filename = self.page_file(channel.id, page, make_dir=True)
            segment = create_segment(channel=channel, series=data)
            with io.open(filename, "wb") as f:
                f.write(segment.SerializeToString())
            self.page_written()
        try:
            if update:
                # modifying an existing page entry
                self.update_page(channel, page, has_data)
            else:
                # adding a new page entry
                self.set_page(channel, page, has_data)
        except sqlite3.OperationalError:
            logger.warn("Indexing DB inaccessible, resetting connection.")
            if self._conn is not None:
                self._conn.close()
            self._conn = None
        except sqlite3.IntegrityError:
            # page already exists - ignore
            pass

    def check_page(self, channel, page):
        """
        Does page exist in cache?
        """
        with self.index_con as con:
            q = """ SELECT page
                    FROM   ts_pages
                    WHERE  channel='{channel}' AND page={page}
            """.format(
                channel=channel.id, page=page
            )
            r = con.execute(q).fetchone()
            return r is not None

    def page_has_data(self, channel, page):
        with self.index_con as con:
            q = """
                SELECT has_data
                FROM   ts_pages
                WHERE  channel='{channel}' AND page={page}
            """.format(
                channel=channel.id, page=page
            )
            r = con.execute(q).fetchone()
            return None if r is None else bool(r[0])

    @require_extension
    def get_page_data(self, channel, page):
        has_data = self.page_has_data(channel, page)
        if has_data is None:
            # page not present in cache
            return None
        elif not has_data:
            # page is empty
            return pd.Series([], index=pd.core.index.DatetimeIndex([]))

        # page has data, let's get it
        filename = self.page_file(channel.id, page, make_dir=True)
        if os.path.exists(filename):
            # get page data from file
            with io.open(filename, "rb") as f:
                series = read_segment(channel, f.read())
            # update access count
            self.update_page(channel, page, has_data)
            return series
        else:
            # page file has been deleted recently?
            logger.warn("Page file not found: {}".format(filename))
            return None

    def update_page(self, channel, page, has_data=True):
        with self.index_con as con:
            q = """
                UPDATE ts_pages
                SET access_count = access_count + 1,
                    last_access  = '{now}',
                    has_data     = {has_data}
                WHERE channel='{channel}' AND page='{page}'
            """.format(
                channel=channel.id,
                page=page,
                has_data=int(has_data),
                now=datetime.now().isoformat(),
            )
            con.execute(q)

    def page_written(self):
        # cache compaction?
        self.write_counter += 1
        if self.write_counter > self.settings.cache_inspect_interval:
            self.write_counter = 0
            self.start_compaction()

    def start_compaction(self, background=True):
        if background:
            # spawn cache compact job
            p = mp.Process(
                target=compact_cache, args=(self, self.settings.cache_max_size)
            )
            p.start()
        else:
            compact_cache(self, self.settings.cache_max_size)

    def remove_pages(self, channel_id, *pages):
        # remove page data files
        for page in pages:
            filename = self.page_file(channel_id, page)
            if os.path.exists(filename):
                os.remove(filename)
            try:
                os.removedirs(os.path.dirname(filename))
            except os.error:
                # directory not empty
                pass
        # remove page index entries
        with self.index_con as con:
            q = """
                DELETE
                FROM ts_pages
                WHERE channel = '{channel}' AND page in ({pages})
            """.format(
                channel=channel_id, pages=",".join(str(p) for p in pages)
            )
            con.execute(q)

    def page_file(self, channel_id, page, make_dir=False):
        """
        Return the file corresponding to a timeseries page (stored as serialized protobuf).
        """
        filedir = os.path.join(self.dir, filter_id(channel_id))
        if make_dir and not os.path.exists(filedir):
            os.makedirs(filedir)
        filename = os.path.join(filedir, "page-{}.bin".format(page))
        return filename

    def clear(self):
        import shutil

        if self._conn is not None:
            with self.index_con as con:
                # remove page entries
                con.execute("DELETE FROM ts_pages;")
                con.commit()
            self._conn.close()
            self._conn = None
        try:
            # delete index file
            os.remove(self.index_loc)
        except:
            logger.warn("Could not delete index file: {}".format(self.index_loc))
        shutil.rmtree(self.dir, ignore_errors=True)
        # reset
        self.init_dir()
        self.init_tables()

    @property
    def page_files(self):
        return glob(os.path.join(self.dir, "*", "*.bin"))

    @property
    def size(self):
        """
        Returns the size of the cache in bytes
        """
        all_files = self.page_files + [self.index_loc]
        return sum(os.stat(x).st_size for x in all_files)


def get_cache(settings, start_compaction=False, init=True):
    cache = Cache(settings)
    if start_compaction:
        background = platform.system().lower() != "windows"
        cache.start_compaction(background=background)
    if init:
        cache.init_tables()
    return cache
