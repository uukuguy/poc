# Public Opinion Cloud
A distributed public opinion analysis framework providing cloud service.

## data_collector
缺省从mongodb://139.196.189.136:27017/获取指定collection中指定开始时间后一分钟内的舆情样本。

目前支持thrift方式访问：

service DataCollector {
    string collect_one_minute_samples(1:string collection_name, 2:i32 year, 3:i32 month, 4:i32 day, 5:i32 hour, 6:i32 minute)
}

./client.py baidu_tieba 2016 1 1 17 55



