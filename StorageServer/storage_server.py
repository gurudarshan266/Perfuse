import sys
import os
import grpc
import itertools
from concurrent import futures
import time

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))
sys.path.append(os.path.abspath(".."))


from defines_pb2 import *
from storageserver_pb2_grpc import *
from db_utils import chunk_database
from constants import *
import chunkserver_pb2_grpc

class storageserver(StorageServerServicer):

    def __init__(self, max_cap):
        self.max_cap = max_cap


    def PushChunkData(self, request_iterator, context):
        db = chunk_database()
        # iter1, iter2 = itertools.tee(request_iterator)
        iter2 = request_iterator
        print "In Push Chunk Data"
        print request_iterator

        c_list = []

        for chunkinfodata in request_iterator:
            # Copy the chunk data only if it is already not present
            if not db.is_chunk_present(chunkinfodata.chunkinfo.hash):
                # Add to DB
                db.add_chunk(chunkinfodata.chunkinfo.hash,chunkinfodata.chunkinfo.len)

                #write to chunk file
                with open(CHUNKS_DIR+chunkinfodata.chunkinfo.hash,"w+") as f:
                    f.write(chunkinfodata.chunkdata.data)

            # TODO: Verify if this change is reflected in the other iterator
            seeder = chunkinfodata.chunkinfo.seeders.add()
            seeder.ip = STORAGE_SERVER_IP
            seeder.port = int(STORAGE_SERVER_PORT)
            seeder.vivaldimetric = chunkinfodata.chunkinfo.seeders[0].vivaldimetric

            c_list.append(chunkinfodata.chunkinfo)

        # Send update to Chunk Server about the chunk info
        # Node info should be added before sending the update to chunk server
        channel = grpc.insecure_channel(CHUNK_SERVER_IP + ":" + CHUNK_SERVER_PORT)
        stub = chunkserver_pb2_grpc.ChunkServerStub(channel)

        print c_list
        x=stub.RouteUpdate(iter(c_list))
        print "got response from server"
        ec = Error()
        ec.ec = 0
        return ec
        


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



    def GetCapacity(self, request, context):
        c = Capacity()
        db = chunk_database()
        c.maxcap = self.max_cap
        c.cursz = db.get_total_size()
        return c




if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    s = storageserver(1*1024*10)

    add_StorageServerServicer_to_server(s, server)
    server.add_insecure_port('[::]:'+str(STORAGE_SERVER_PORT))
    server.start()
    _ONE_DAY_IN_SECONDS = 24*60*60
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)







