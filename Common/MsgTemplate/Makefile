all:
	python -m grpc_tools.protoc -Isrc/ --python_out=PyTemplate/ --grpc_python_out=PyTemplate/ src/chunkserver.proto src/request.proto src/response.proto src/defines.proto
clean:
	rm -rf PyTemplate/*	
