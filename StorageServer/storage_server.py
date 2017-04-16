import sys
import os
import grpc
import itertools
from concurrent import futures

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))


from defines_pb2 import *
from storageserver_pb2_grpc import *
from db_utils import chunk_database
from constants import *
import chunkserver_pb2_grpc

class storageserver(StorageServerServicer):

    def PushChunkData(self, request_iterator, context):
        db = chunk_database()
        iter1, iter2 = itertools.tee(request_iterator)

        for chunkinfodata in iter1:
            # Copy the chunk data only if it is already not present
            if not db.is_chunk_present(chunkinfodata.hash):
            # Add to DB
                db.add_chunk(chunkinfodata.hash,chunkinfodata.len)

                #write to chunk file
                with open(CHUNKS_DIR+chunkinfodata.hash,"w+") as f:
                    f.write(chunkinfodata.chunkdata.data)

                # TODO: Verify if this change is reflected in the other iterator
                seeder = chunkinfodata.chunkinfo.seeders.add()
                seeder.ip = STORAGE_SERVER_IP
                seeder.port = STORAGE_SERVER_PORT

        # Send update to Chunk Server about the chunk info
        # Node info should be added before sending the update to chunk server
        channel = grpc.insecure_channel(CHUNK_SERVER_IP + ":" + CHUNK_SERVER_PORT)
        stub = chunkserver_pb2_grpc.ChunkServerStub(channel)
        stub.RouteUpdate(iter2)
        


    def GetChunkData(self, request, context):
        db = chunk_database()
        chunk_data = ChunkData()

        if not db.is_chunk_present(request.hash):
            chunk_data.data = None
            return chunk_data

        with open(CHUNKS_DIR+request.hash, "r") as f:
            s = f.read()


        chunk_data.data = s

        return chunk_data



if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    s = storageserver()

    chunkserver_pb2_grpc.add_StorageServerServicer_to_server(s, server)
    server.add_insecure_port('[::]:'+STORAGE_SERVER_PORT)
    server.start()







