from request_pb2 import *
from defines_pb2 import *
import os.path
from db_utils import *
from file_splicer_utils import *

def get_parent_dir(filenm):
    if filenm=='/':
        return 'NO_ROOT'
    return os.path.abspath(os.path.join(filenm, os.pardir))

def request_file_hashes(reqid, filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETHASHES
    r.filename = filenm
    r.parent = get_parent_dir(filenm)
    return r


def request_dir_info(reqid,dirnm):
    r = Request()
    r.reqid = reqid
    r.method = GETDIRLIST
    r.filename = dirnm
    r.parent = get_parent_dir(dirnm)
    return r


def request_file_info(reqid,filenm):
    r = Request()
    r.reqid = reqid
    r.method = GETFILEINFO
    r.filename = filenm
    r.parent = get_parent_dir(filenm)
    return r


def request_write_chunk(reqid,filenm):
    r = Request()
    r.reqid = reqid
    r.method = WRITECHUNK
    r.filename = filenm
    r.parent = get_parent_dir(filenm)

    return r

def request_update_fileinfo(reqid,filenm,sz,m_time,is_dir):
    r = Request()
    r.reqid = reqid
    r.method = UPDATEFILEINFO
    r.filename = filenm
    r.parent = get_parent_dir(filenm)

    finfo = r.fileinfo
    finfo.filename = filenm
    finfo.size = sz
    finfo.lastmodified = m_time
    finfo.is_dir = is_dir
    finfo.parent = get_parent_dir(filenm)
    return r

def request_remove_file(reqid,filenm,is_dir):
    r = Request()
    r.reqid = reqid
    r.method = REMOVEFILE
    r.filename = filenm
    r.parent = get_parent_dir(filenm)

    finfo = r.fileinfo
    finfo.filename = filenm
    finfo.size = 0
    finfo.lastmodified = to_utc(1492144252)
    finfo.is_dir = is_dir
    finfo.parent = get_parent_dir(filenm)
    mtime = 1492144252
    return r


