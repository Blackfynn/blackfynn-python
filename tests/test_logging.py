import logging
import os


def test_default_log_level():
    import blackfynn.log as log

    # default log level should be INFO
    base_log = log.get_logger("base_log")
    assert base_log.getEffectiveLevel() == logging.INFO


def test_log_level_based_on_env():
    import blackfynn.log as log

    # setting env var should change logging level
    os.environ["BLACKFYNN_LOG_LEVEL"] = "WARN"
    warn_log = log.get_logger("warn_log")
    assert warn_log.getEffectiveLevel() == logging.WARN
