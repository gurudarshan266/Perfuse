from concurrent import futures
import sys
import os

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))

import time
import grpc
from defines_pb2 import *

import chunkserver_pb2_grpc
from request_pb2 import *
from response_pb2 import *
from defines_pb2 import *

from hash_utils import *
from db_utils import *
import constants
from requestpb_utils import *
from responsepb_utils import *

import glob

channel = grpc.insecure_channel(constants.CHUNK_SERVER_IP+":"+str(constants.CHUNK_SERVER_PORT))
stub = chunkserver_pb2_grpc.ChunkServerStub(channel)

file = "RFC882"

#simulate open call
db = chunk_database()
req = request_file_hashes(1,file)
print("open()\n")
# print(req)
resp = stub.GetResponse(req)
# print(resp)

#simulate readdir
req = request_dir_info(2,".")
print("readdir()\n")
resp = stub.GetResponse(req)
print(resp.filesinfo[1])
