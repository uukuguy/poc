
all: data_collector

data_collector: data_collector.thrift
	thrift -gen py data_collector.thrift

clean:
	rm -fr gen-py

