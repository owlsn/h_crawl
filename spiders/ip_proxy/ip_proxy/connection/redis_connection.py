# -*- coding: utf-8 -*-
import redis
from ip_proxy.config import REDIS
import traceback
import logging
import time
import json

# redis连接池
class RedisConnection(object):

    def __init__(self):
        try:
            self.config = REDIS
            self.pool = redis.ConnectionPool(host = self.config['host'], port = self.config['port'],
            db = self.config['db'], password = self.config['password'])
            self.conn = redis.Redis(connection_pool = self.pool)
            pass
        except Exception as e:
            logger = logging.getLogger()
            logger.error(traceback.format_exc())
            pass
            
