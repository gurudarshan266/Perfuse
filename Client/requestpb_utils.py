from request_pb2 import *
from defines_pb2 import *

def request_file_hashes(reqid, filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETHASHES;
    r.filename = filenm
    return r

def request_dir_info(reqid,dirnm):
    r = Request()
    r.reqid = reqid
    r.method = GETDIRLIST
    r.filename = dirnm
    return r

def request_file_info(reqid,filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETFILEINFO
    r.filename = filenm
    return r

