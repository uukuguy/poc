#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
data_collector.py
'''
from __future__ import division
import sys
sys.path.append('..')

import os
from os import path
import time
import logging
from utils.logger import Logger, AppWatch

import msgpack
import pymongo

from io import BytesIO

# ---------------- do_collection() ----------------
def do_collection(collection, start_date, end_date):

    result_data = BytesIO()

    condition = {'result.publish_time': {'$gte': start_date, '$lte': end_date}}
    logging.info('search: {},{}'.format(collection.name, condition))

    total_samples = 0
    total_size = 0;
    #batch_content = leveldb.WriteBatch()
    for item in collection.find(condition):
        text = item['result']['text'].encode('utf-8')
        if len(text) == 0:
            continue

        url = item['url'].encode('utf-8')
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['result']['publish_time']))
        title = item['result'].get('title', '').encode('utf-8')
        sample_type = item['result']['type'].encode('utf-8')
        keyword = item['result']['extra'].get('keyword', '').encode('utf-8')

        sample = (url, sample_type, publish_time, url, keyword, title, text)
        sample_data = msgpack.packb(sample)
        total_size += len(sample_data)

        result_data.write(sample_data)

        total_samples += 1
        logging.debug(Logger.debug("%d [%s] %d %s" % (total_samples, publish_time, len(sample_data), title)))
        #sample_id = self.acquire_sample_id(1)
        #if sample_id % 1000 == 0:
            #print sample_id, title
        #sample_data = (sample_id, title, content)
        #rowstr = msgpack.dumps(sample_data)
        #batch_content.Put(str(sample_id), rowstr)

    #self.db.Write(batch_content, sync=True)

    logging.info(Logger.notice("Collected %d samples (size = %.3f MB)." % (total_samples, total_size / (1024 * 1024))))

    return result_data.getvalue()

# ---------------- collect_one_minute_samples() ----------------
def collect_one_minute_samples(mongodb, db_name, collection_name, (year, month, day, hour, minute)):
    mongo_client = pymongo.MongoClient(mongodb) # mongodb://139.196.189.136:27017/
    db = mongo_client[db_name]
    start_date = int(time.mktime(map(eval, "{}-{}-{}-{}-{}-00-0-0-0".format(year, month, day, hour, minute).split('-'))))
    end_date = int(time.mktime(map(eval, "{}-{}-{}-{}-{}-59-0-0-0".format(year, month, day, hour, minute).split('-'))))

    if type(collection_name) is list:
        result_data = None
        for col_name in collection_name:
            collection = db.get_collection(col_name)
            sub_result = do_collection(collection, start_date, end_date)
            result_data += sub_result
        return result_data
    else:
        collection = db.get_collection(collection_name)
        return do_collection(collection, start_date, end_date)

def main():
    mongodb = 'mongodb://139.196.189.136:27017/'
    db_name = 'resultdb'
    collection_name = 'baidu_tieba'
    collect_one_minute_samples(mongodb, db_name, collection_name, 2016, 1, 1, 7, 18);

if __name__ == '__main__':
    appwatch = AppWatch()
    main()
    appwatch.stop()

