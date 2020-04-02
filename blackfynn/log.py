from __future__ import absolute_import, division, print_function

import logging
import os

logging.basicConfig()


def get_logger(name="blackfynn-python"):
    """
    Returns a logger configured to be used throughout the
    blackfynn-python library

    Args:
      name (string): Name of the logger, default "blackfynn-python"

    Returns:
      Logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("BLACKFYNN_LOG_LEVEL", "INFO"))

    return logger
