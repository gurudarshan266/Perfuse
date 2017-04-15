import sys
import os
import grpc

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))


from defines_pb2 import *
from storageserver_pb2_grpc import *
from db_utils import chunk_database
from constants import *

class storageserver(StorageServerServicer):

    def PushChunkData(self, request, context):
        db = chunk_database()
        chunkinfo = request.chunkinfo;

        #Copy the chunk data only if it is already not present
        if not db.is_chunk_present(chunkinfo.hash):
            #add to DB
            db.add_chunk(chunkinfo.hash,chunkinfo.len)

            #write to chunk file
            with open(CHUNKS_DIR+chunkinfo.hash,"w+") as f:
                f.write(request.chunkdata.data)

        #TODO: Send update to Chunk Server about the chunk info

