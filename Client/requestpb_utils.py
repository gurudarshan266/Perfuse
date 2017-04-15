from request_pb2 import *
from defines_pb2 import *
import os.path
from db_utils import *


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
    r.parent = os.path.abspath(os.path.join(dirnm, os.pardir))
    return r


def request_file_info(reqid,filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETFILEINFO
    r.filename = filenm
    r.parent = os.path.abspath(os.path.join(filenm, os.pardir))
    return r


def request_write_chunk(reqid,filenm):
    r = Request()
    r.reqid = reqid
    r.method = WRITECHUNK
    r.filename = filenm
    r.parent = os.path.abspath(os.path.join(filenm, os.pardir))

    return r
