from hash_utils import *
from db_utils import chunk_database
from  constants import *
import os

def splice_file(db, filenm, pseudofilenm="", write_to_chunkfile=False):
    if pseudofilenm == "":
        pseudofilenm = filenm
    bytes_read = 0
    with open(filenm) as f:
        file_sz = os.path.getsize(filenm)
        while bytes_read < file_sz:
            data = f.read(CHUNK_SIZE)
            sz = len(data)
            hash = compute_hash(data)
            is_present = db.is_chunk_present(hash)
            db.add_chunk(hash, pseudofilenm, bytes_read, sz)
            bytes_read = bytes_read + sz
            if (not is_present) and write_to_chunkfile:
                with open("chunks/"+hash,"w+") as fc:
                    fc.write(data)


def get_chunk_list(db, filenm, offset, len):
    start = offset
    end = offset + len
    chunks_file = db.get_chunks_for_file(filenm)
    chunks_list = []
    # print(chunks_file)
    for c in chunks_file:
        if(start<(c[OFFSET_INDEX]+c[LEN_INDEX]) and end>(c[OFFSET_INDEX])):
            chunks_list.append(c)
    return chunks_list

def get_chunk_data(hash,offset,len):
    with open("chunks/"+hash) as f:
        f.seek(offset)
        data = f.read(len)
    return data

def get_chunks_data(chunks_list, offset, len):
    start = offset
    end = offset+len-1
    data = ""
    for c in chunks_list:
        if(start>end):
            break
        len_chunk = min(c[OFFSET_INDEX]+c[LEN_INDEX],end+1)-start
        s = get_chunk_data(c[HASH_INDEX],start-c[OFFSET_INDEX],len_chunk)
        start = c[OFFSET_INDEX]+c[LEN_INDEX]
        data = data + s
    return data


# file = "scaffold/files/RFC882"
# db = chunk_database()
# db.create_table()
# splice_file(db, file,"RFC882",True)
#
# lst = get_chunk_list(db,"RFC882",3000,4096)
# data = get_chunks_data(lst,3000,4096)
# print len(data)

