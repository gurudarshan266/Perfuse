from request_pb2 import *
from defines_pb2 import *

def request_file_hashes(reqid, filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETHASHES;
    r.filename = filenm
    return r

