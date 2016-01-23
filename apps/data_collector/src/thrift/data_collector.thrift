service DataCollector {
    string collect_one_minute_samples(1:string collection_name, 2:i32 year, 3:i32 month, 4:i32 day, 5:i32 hour, 6:i32 minute)
}

