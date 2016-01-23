
all: data_collector

python:
	mkdir -p python

data_collector: python data_collector.thrift
	thrift -gen py -out python data_collector.thrift

clean:
	rm -fr python

