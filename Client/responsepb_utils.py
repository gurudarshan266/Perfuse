from response_pb2 import *
from defines_pb2 import *

import db_utils

def add_chunk_to_db(db,chunk):
    db.add_chunk_to_db(chunk.hash, chunk.filename, chunk.offset,chunk.len)

def add_file_hashes_to_db(db,resp):

    if resp.method != GETHASHES:
        return

    for chunk in resp.chunksinfo:
        add_chunk_to_db(db,chunk)