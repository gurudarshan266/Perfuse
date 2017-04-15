all:
	python -m grpc_tools.protoc -I../../Chunkserver/src/main/proto/ --python_out=PyTemplate/ --grpc_python_out=PyTemplate/ ../../Chunkserver/src/main/proto/*.proto
clean:
	rm -rf PyTemplate/*	
