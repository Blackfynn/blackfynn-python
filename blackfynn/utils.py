# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from future.utils import integer_types, string_types

import datetime

from blackfynn.extensions import numpy as np
from blackfynn.extensions import pandas as pd
from blackfynn.extensions import require_extension

# data type helpers


def value_as_type(value, dtype):
    try:
        if dtype == "string":
            return str(value)
        elif dtype == "integer":
            return int(value)
        elif dtype == "double":
            return float(value)
        elif dtype == "date":
            return infer_epoch_msecs(value)
        if dtype == "boolean":
            return value.lower() == "true"
    except:
        raise Exception("Unable to set value={} as type {}".format(value, dtype))


def get_data_type(v):
    """
    Infers type from value. Returns tuple of (type, value)
    """
    if isinstance(v, datetime.datetime):
        return ("date", msecs_since_epoch(v))
    elif isinstance(v, bool):
        return ("boolean", str(v).lower())
    elif isinstance(v, float):
        return ("double", v)
    elif isinstance(v, integer_types):
        return ("integer", v)
    else:
        # infer via casting
        if is_integer(v):
            return ("integer", int(v))
        elif is_decimal(v):
            return ("double", float(v))
        else:
            return ("string", str(v))


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_decimal(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# time-series helpers


def infer_epoch_msecs(thing):
    if isinstance(thing, datetime.datetime):
        return msecs_since_epoch(thing)
    elif isinstance(thing, (integer_types, float)):
        # assume milliseconds
        return int(thing)
    elif isinstance(thing, string_types):
        # attempt to convert to msec integer
        return int(thing)
    else:
        raise Exception("Cannot parse date")


def infer_epoch(thing):
    if isinstance(thing, datetime.datetime):
        return usecs_since_epoch(thing)
    elif isinstance(thing, (integer_types, float)):
        # assume microseconds
        return int(thing)
    else:
        raise Exception("Cannot parse date")


def secs_since_epoch(the_time):
    the_time = the_time.replace(tzinfo=None)
    # seconds from epoch (float)
    return (the_time - datetime.datetime.utcfromtimestamp(0)).total_seconds()


def msecs_since_epoch(the_time):
    # milliseconds from epoch (integer)
    return int(secs_since_epoch(the_time) * 1000)


def usecs_since_epoch(the_time):
    # microseconds from epoch (integer)
    return int(secs_since_epoch(the_time) * 1e6)


def usecs_to_datetime(us):
    # convert usecs since epoch to proper datetime object
    return datetime.datetime.utcfromtimestamp(0) + datetime.timedelta(
        microseconds=int(us)
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Timeseries helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@require_extension
def generate_data(size, func="walk", scale=5, periods=10):

    remainder = size % periods
    pattern_length = int(size / periods)
    if func == "walk":
        x = (np.random.rand(size) - 0.5).cumsum()
        # normalize to [-scale,scale]
        return x / np.max([x.min(), x.max()]) * scale
    elif func == "sin":
        return np.sin(np.linspace(0, np.pi * periods, size)) * scale
    elif func == "square":
        pattern = np.concatenate(
            [np.ones(pattern_length // 2) * -1, np.ones(pattern_length // 2)]
        )
        return (
            np.concatenate([np.repeat(pattern, periods), pattern[:remainder]]) * scale
        )
    elif func == "sawtooth":
        pattern = np.linspace(-scale, scale, pattern_length)
        return np.concatenate([np.repeat(pattern, periods), pattern[:remainder]])


@require_extension
def generate_dataframe(minutes=2, freq=100):

    start = datetime.datetime(2017, 1, 1, 0, 0)
    end = start + datetime.timedelta(minutes=minutes)

    # index
    ind = pd.date_range(start=start, end=end, freq="10000u", closed="left")
    n = len(ind)

    # dataframe
    return pd.DataFrame(
        {
            "random-walk": generate_data(n, func="walk"),
            "sin": generate_data(n, func="sin"),
            "sawtooth": generate_data(n, func="sawtooth"),
            "square": generate_data(n, func="square"),
        },
        index=ind,
    )
