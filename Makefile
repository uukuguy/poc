
.PHONY: data_collector

all: data_collector

data_collector: 
	make -C src/data_collector
	
clean:
	make -C src/data_collector clean
	make -C src/utils clean

