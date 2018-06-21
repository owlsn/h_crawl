# coding = utf-8
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.connection.mysql_connection import MysqlConnection
from ip_proxy.config import QUEUE_NUM
import traceback
from ip_proxy.utils.log import log
import time

class IpQueue(object):

    def __init__(self):
        r = RedisConnection(db = 1)
        self.redis = r.conn
        m = MysqlConnection(type = 'syn')
        self.mysql = m.conn
        pass

    def getQueue(self, level):
        key = 'ip_queue_' + str(level)
        return key

    def do_select(self):
        try:
            logger = log.getLogger('development')
            timeArray = time.localtime(time.time())
            date_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            logger.info('ip_queue start at:{}'.format(date_time))
            
            for i in range(QUEUE_NUM):
                length = self.redis.llen(self.getQueue(i))
                if length < 10000:
                    sql = """select ip, port, scheme, level, flag from `ip` where level = %s order by update_time asc"""
                    params = (i)
                    cursor = self.mysql.cursor()
                    cursor.execute(sql, params)
                    res = cursor.fetchall()
                    for value in res:
                        data = {'ip' : value[0], 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4]}
                        if data['level'] is not None:
                            self.redis.rpush(self.getQueue(data['level']), data)
                        else:
                            self.redis.rpush(self.getQueue(0), data)
            pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc())
            pass

ip_queue = IpQueue()