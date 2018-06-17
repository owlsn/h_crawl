# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
import socket
import struct

class IpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    isp = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    scheme = scrapy.Field()

    def get_insert_sql(self):
        if not 'scheme' in self.keys() or self['scheme']:
            self['scheme'] = 'http'
        if 'ip' in self.keys() and self['ip'] and 'port' in self.keys() and self['port']:
            insert_sql = """insert into `ip` (`ip`, `port`, `create_time`, `scheme`, `delay`, `level`) values (%s, %s, %s, %s, %s, %s);"""
            params = (struct.unpack('!I', socket.inet_aton(self['ip']))[0], self['port'], time.time(), self['scheme'], -1, 0)
            return insert_sql, params
        else:
            return None
            