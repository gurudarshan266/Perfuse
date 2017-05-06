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
from time import time,sleep

class storageserver(StorageServerServicer):

    def __init__(self, max_cap,cs_ip):
        self.chunserver_ip = cs_ip
        self.max_cap = max_cap


    def PushChunkData(self, request_iterator, context):
        db = chunk_database()
        # iter1, iter2 = itertools.tee(request_iterator)
        iter2 = request_iterator
	start_time = time()
        #print "In Push Chunk Data"
        # print request_iterator

        c_list = []

        for chunkinfodata in request_iterator:
            # Copy the chunk data only if it is already not present
	   # print("\n\n 1.Before checking for chunk in DB @ %s"%str(time()-start_time))
            if not db.is_chunk_present(chunkinfodata.chunkinfo.hash):
                # Add to DB
                db.add_chunk(chunkinfodata.chunkinfo.hash,chunkinfodata.chunkinfo.len)

	    #	print("2. After checking for chunk in DB @ %s"%str(time()-start_time))
                #write to chunk file
                with open(CHUNKS_DIR+chunkinfodata.chunkinfo.hash,"w+") as f:
                    f.write(chunkinfodata.chunkdata.data)
	#	print("3. Done with writing chunk @ %s"%str(time()-start_time))

            # TODO: Verify if this change is reflected in the other iterator
#            seeder = chunkinfodata.chunkinfo.seeders[0]#.add()
 #           seeder.ip = STORAGE_SERVER_IP
  #          seeder.port = int(STORAGE_SERVER_PORT)
   #         seeder.vivaldimetric = chunkinfodata.chunkinfo.seeders[0].vivaldimetric

	 #   print("4. Before appending @ %s"%str(time()-start_time))
            c_list.append(chunkinfodata.chunkinfo)
	  #  print("5. After appending @ %s"%str(time()-start_time))
	#print("6. Done writing to files @ %s"%str(time()-start_time))
        # Send update to Chunk Server about the chunk info
        # Node info should be added before sending the update to chunk server
        channel = grpc.insecure_channel(self.chunserver_ip + ":" + CHUNK_SERVER_PORT)
        stub = chunkserver_pb2_grpc.ChunkServerStub(channel)

        # print c_list
        x=stub.RouteUpdate(iter(c_list))
        #print "7. got response from server @ %s"%str(time()-start_time)
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
    cs_ip = CHUNK_SERVER_IP

    if len(sys.argv)>=2:
        cs_ip = sys.argv[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    s = storageserver(1*1024*10, cs_ip)

    add_StorageServerServicer_to_server(s, server)
    server.add_insecure_port('[::]:'+str(STORAGE_SERVER_PORT))
    server.start()
    _ONE_DAY_IN_SECONDS = 24*60*60
    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)







