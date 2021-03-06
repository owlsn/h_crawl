# coding = utf-8

import logging
from logging import config
from display.config import LOG_CONFIG

class Log(object):
    
    def __init__(self):
        self.logging = logging
        if LOG_CONFIG:
            self.config = LOG_CONFIG
            self.logging.config.dictConfig(LOG_CONFIG)
        else:
            self.logging.basicConfig(level = logging.INFO)

    def getLogger(self, logger):
        return self.logging.getLogger(logger)