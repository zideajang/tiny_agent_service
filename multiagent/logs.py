#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from loguru import logger as _logger
from azentengine.const import PROJECT_ROOT


def define_log_level(print_level="INFO", logfile_level="DEBUG"):
    _logger.add(sys.stderr, level=print_level)
    _logger.add(PROJECT_ROOT / 'logs/log.txt', level=logfile_level)
    return _logger


logger = define_log_level()


if __name__ == "__main__":
    logger.info("hello world")