from concurrent import futures
import sys
import os

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))

import time
import grpc
from defines_pb2 import *

from chunkserver_pb2_grpc import *
from request_pb2 import *
from response_pb2 import *

from hash_utils import *
from db_utils import *

import glob

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class mychunkserver(ChunkServerServicer):
    "Temporary server"

    def GetResponse(self, request, context):
        db = chunk_database()

        resp = Response()
        resp.respid = request.reqid
        resp.method = request.method

        if (request.method == GETHASHES):
            rows = db.get_chunks_for_file("files/"+request.filename)
            print rows
            for r in rows:
                c = resp.chunksinfo.add()
                c.hash = r[1]
                c.filename = r[2]
                c.offset = r[3]
                c.len = r[4]

        print(resp)
        return resp

    def attach_db(self,db):
        self.db = db

def add_files_to_db(db):
    file_list = glob.glob("files/*")
    for file in file_list:
        with open(file,"r") as f:
            s = f.read()
            hash = compute_hash(s)
            db.add_chunk(hash, file, offset=0, length=len(s))


def serve():
  db = chunk_database("files.db")
  db.create_table()
  add_files_to_db(db)

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  c = mychunkserver()

  add_ChunkServerServicer_to_server(c, server)
  server.add_insecure_port('[::]:5001')
  server.start()


  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()


