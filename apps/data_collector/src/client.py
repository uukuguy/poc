#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
client.py

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
import msgpack

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import DataCollector
from io import BytesIO

sys.path.append(sys.path[0] + '/' + '..')
from utils.logger import Logger, AppWatch


DATACOLLECTOR_IP = '127.0.0.1'
PORT = 20161

def main():
    if len(sys.argv) != 7:
        print "Usage: sys.argv[0] <collection_name> <year> <month> <day> <hour> <minute>"
        print "       collection_name: 'baidu_tieba'"
        exit(-1)

    collection_name = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    day = int(sys.argv[4])
    hour = int(sys.argv[5])
    minute = int(sys.argv[6])

    try:
        sock = TSocket.TSocket(DATACOLLECTOR_IP, PORT)
        transport = TTransport.TBufferedTransport(sock)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = DataCollector.Client(protocol)

        transport.open()

        return_data = client.collect_one_minute_samples(collection_name, year, month, day, hour, minute)

        unpacker = msgpack.Unpacker(BytesIO(return_data))
        for unpacked in unpacker:
            (url, sample_type, publish_time, url, keyword, title, text) = unpacked
            print publish_time, sample_type, title

        transport.close()

    except Thrift.TException, tx:
        print 'Exception: %s' % (tx.message)


if __name__ == '__main__':
    appwatch = AppWatch()
    main()
    appwatch.stop()

