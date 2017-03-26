from concurrent import futures
import sys
import os

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))

import time
import grpc

from chunkserver_pb2_grpc import *
from request_pb2 import *
from response_pb2 import *


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class myserver(ChunkServerServicer):
	"Temporary server"
	def GetResponse(self, request, context):
		resp = Response()
		resp.respid = request.reqid;
		resp.method = request.method;


		return resp


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_ChunkServerServicer_to_server(myserver(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()


