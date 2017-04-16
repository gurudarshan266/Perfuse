from response_pb2 import *
from defines_pb2 import *
from db_utils import *
from constants import *
from storageserver_pb2 import *
import storageserver_pb2_grpc

import grpc
import os.path
import time

def is_chunkfile_present(hash):
    return os.path.isfile(CHUNKS_DIR + hash)

def add_chunk_to_db(db,chunk):
    #TODO: Get the node with the lowest vivaldi metric
    ssip = chunk.seeders[0].ip
    ssport = chunk.seeders[0].port
    db.add_chunk_to_db(chunk.hash, chunk.filename, chunk.offset, chunk.len, ssip, ssport)
    #If chunk file already present, update the value in the table
    if is_chunkfile_present(chunk.hash):
        db.set_incache(chunk.hash, True)

def add_file_hashes_to_db(db,resp):

    if resp.method != GETHASHES:
        return

    for chunk in resp.chunksinfo:
        add_chunk_to_db(db,chunk)


def push_chunks_to_storage_server(resp,filenm):
    print resp
    #Extract the storage server port and IP
    ss_ip = resp.seeders[0].ip
    ss_port = str(resp.seeders[0].port)

    #create channel and stub to the storage server
    ss_channel = grpc.insecure_channel(ss_ip+':'+ss_port)
    ss_stub = storageserver_pb2_grpc.StorageServerStub(ss_channel)

    #connect to DB
    db = chunk_database()

    # Get the chunks from DB
    chunks_sql= db.get_chunks_for_file(filenm)

    #Send data to Storage Server
    iterator = get_chunk_iterator(chunks_sql)
    ec = ss_stub.PushChunkData(iterator)
    print "EC = %d"%ec.ec

def get_chunk_iterator(chunks_sql):
    
    for c in chunks_sql:

        chunk_info_data = ChunkInfoData()

        #Extract Data into ChunkInfo object
        c_info = chunk_info_data.chunkinfo
        c_info.hash = c[1]
        c_info.filename = c[2]
        c_info.offset = c[3]
        c_info.len = c[4]
        seeder = c_info.seeders.add()
        seeder.ip = "localhosts"
        seeder.port = 50004
        seeder.vivaldimetric = 100

        #Fetch the data from the chunk file and save it inside ChunkData()
        c_data = chunk_info_data.chunkdata
        with open(CHUNKS_DIR+c_info.hash, "r") as f:
            c_data.data = f.read()

        #Create ChunkInfoData object to send to Storage server
        # chunk_info_data.chunkdata = c_data

        print chunk_info_data
        yield chunk_info_data
        time.sleep(0.5)


