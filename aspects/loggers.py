# coding=utf-8
"""
Created on 2020, June 9th
@author: orion
"""
import os
import logging
from logging import FileHandler
from logging import Formatter

from .constants import ASPECTS_OUTPUTS

# VENUS

LOG_FORMAT = '%(asctime)s, %(levelname)s %(message)s'
LOG_LEVEL = logging.INFO

LOG_NAME = "SEARCH ASPECTS"


def get_logger(suffix=""):
    log_name = LOG_NAME.replace(" ", '.').lower()
    filename = "{}.{}".format(log_name, suffix) if suffix else log_name
    log_file = os.path.join(
        ASPECTS_OUTPUTS,
        "{}.log".format(filename),
    )
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(LOG_LEVEL)
    logger_file_handler = FileHandler(
        log_file,
    )
    logger_file_handler.setLevel(LOG_LEVEL)
    logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
    logger.addHandler(logger_file_handler)

    return logger
