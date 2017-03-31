from hash_utils import *
from db_utils import chunk_database
import constants
import os

def splice_file(db, filenm, pseudofilenm="", write_to_chunkfile=False):
    if pseudofilenm == "":
        pseudofilenm = filenm
    bytes_read = 0
    with open(filenm) as f:
        file_sz = os.path.getsize(filenm)
        while bytes_read < file_sz:
            data = f.read(constants.CHUNK_SIZE)
            sz = len(data)
            hash = compute_hash(data)
            is_present = db.is_chunk_present(hash)
            db.add_chunk(hash, pseudofilenm, bytes_read, sz)
            bytes_read = bytes_read + sz
            if (not is_present) and write_to_chunkfile:
                with open("chunks/"+hash,"w+") as fc:
                    fc.write(data)

# file = "scaffold/files/RFC882"
# db = chunk_database()
# splice_file(db, file,"RFC882",True)