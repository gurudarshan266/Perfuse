import sys
import os
import grpc
import itertools

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))


from defines_pb2 import *
from storageserver_pb2_grpc import *
from db_utils import chunk_database
from constants import *

class storageserver(StorageServerServicer):

    def PushChunkData(self, request_iterator, context):
        db = chunk_database()
        iter1, iter2 = itertools.tee(request_iterator)
        for chunkinfo in iter1:
        #Copy the chunk data only if it is already not present

            if not db.is_chunk_present(chunkinfo.hash):
            #add to DB
                db.add_chunk(chunkinfo.hash,chunkinfo.len)

                #write to chunk file
                with open(CHUNKS_DIR+chunkinfo.hash,"w+") as f:
                    f.write(request.chunkdata.data)

        #TODO: Send update to Chunk Server about the chunk info
        channel = grpc.insecure_channel(CHUNK_SERVER_IP + ":" + CHUNK_SERVER_PORT)
        stub = chunkserver_pb2_grpc.ChunkServerStub(channel)
        stub.RouteUpdate(iter2)
        


    def GetChunkData(self, request, context):
        db = chunk_database()

        if not db.is_chunk_present(request.hash):
            return None

        with open(CHUNKS_DIR+request.hash, "r") as f:
            s = f.read()


        chunk_data = ChunkData()
        chunk_data.data = s

        return chunk_data







