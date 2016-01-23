
all: 
	make -C src
	
clean:
	make -C src clean
	make -C utils clean

build-image:
	docker build -t udb/data_collector:1 .

run:
	docker run -d --name dc1 -p 20161:20161 udb/data_collector:1

