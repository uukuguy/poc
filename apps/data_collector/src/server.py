#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
server.py

    目前mongodb数据集合有

    baidu_site_search 百度网页搜索
    baidu_tieba  百度贴吧
    common 指定的4000个站点采集
    hotpoint_baidu  百度热点
    hotword_baidu  百度热词
    news_360  360搜索
    news_baidu  百度新闻
    news_sougou  搜狗新闻
    sougou_wenxin 搜狗微信
    weibo_qq 腾讯微博
    weibo_sina 新浪微博
    weibo_renmin 人民网微博
    weibo_xinhua 新华网微博

'''
import sys
sys.path.append(sys.path[0] + '/' + './thrift/gen-py/data_collector')

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
#from thrift.server import TNonblockingServer
from thrift.server import TProcessPoolServer

import DataCollector

sys.path.append(sys.path[0] + '/' + '..')
from utils.logger import Logger, AppWatch

import data_collector

MONGODB = 'mongodb://139.196.189.136:27017/'
DBNAME = 'resultdb'
PORT = 20161

class DataCollectorHandler():
    def __init__(self):
        pass

    def collect_one_minute_samples(self, collection_name, year, month, day, hour, minute):
        mongodb = MONGODB
        db_name = DBNAME
        return data_collector.collect_one_minute_samples(mongodb, db_name, collection_name, (year, month, day, hour, minute))

def main():
    handler = DataCollectorHandler()
    processor = DataCollector.Processor(handler)
    transport = TSocket.TServerSocket(host=None, port=PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)

    server.serve()

if __name__ == '__main__':
    appwatch = AppWatch()
    main()
    appwatch.stop()


