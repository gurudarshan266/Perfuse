#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging
import sys
import os

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))

from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock
from stat import *

from fusepy.fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from requestpb_utils import *
from responsepb_utils import *
import constants
import chunkserver_pb2_grpc
from db_utils import *
from file_splicer_utils import *

class Loopback(LoggingMixIn, Operations):
    def __init__(self, root):
        self.root = realpath(root)
        self.rwlock = Lock()

        self.req_cnt = 0

        #Connect to server
        self.channel = grpc.insecure_channel(constants.CHUNK_SERVER_IP+":"+str(constants.CHUNK_SERVER_PORT))
        self.stub = chunkserver_pb2_grpc.ChunkServerStub(self.channel)

        self.tmp_files = {}
        self.tmpfiles_id = 0

        # self.db = chunk_database()


    def __call__(self, op, path, *args):
        return super(Loopback, self).__call__(op, path, *args)

    def access(self, path, mode):
        pass
        # if not os.access(path, mode):
        #     raise FuseOSError(EACCES)

    chmod = os.chmod
    chown = os.chown

    def create(self, path, mode):
        #TODO:check if the path exists and the parent is a directory
        tmp_filenm = TMP_DIR+"file"+self.tmpfiles_id
        self.tmpfiles_id = self.tmpfiles_id + 1
        self.tmp_files[path] = tmp_filenm
        f=open(tmp_filenm,'w+')
        f.close()

        #return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)

    #TODO: Need to splice the files at this stage while writing
    def flush(self, path, fh):
        return 0
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        if datasync != 0:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def getattr(self, path, fh=None):
        if(path=="/.Trash" or path=="/.Trash-1000"):
            raise FuseOSError(EACCES)

        self.req_cnt = self.req_cnt + 1

        req = request_file_info(self.req_cnt, path)
        resp = self.stub.GetResponse(req)
        # attr = dict()float(file.lastmodified)#to be changed
        st = os.lstat("foo")
        attr =  dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime','st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

        if(len(resp.filesinfo)>0):
            file = resp.filesinfo[0]  # Only the first entry is required
            attr['st_mtime'] = float(file.lastmodified)
            attr['st_ctime'] = float(file.lastmodified)#to be changed
            attr['st_atime'] = float(file.lastmodified)#to be changed
            attr['st_size'] = file.size
            attr['st_mode'] = 0777 | (S_IFREG if not file.is_dir else S_IFDIR)
        return attr

    getxattr = None

    def link(self, target, source):
        return os.link(source, target)

    listxattr = None
    mkdir = os.mkdir
    mknod = os.mknod
    #open = os.open



    def open(self, file, mode):
        self.req_cnt = self.req_cnt + 1
        # return 5
        req = request_file_hashes(self.req_cnt,file)
        print(req)
        resp = self.stub.GetResponse(req)
        print(resp)
        add_file_hashes_to_db(self.db,resp)



    def read(self, path, size, offset, fh):
        print("Path = %s, Len = %d, Offset = %d"%(path,size,offset))
        data = ''
        # Directly read from a file when it is newly created
        if path in self.tmp_files:
            with open(self.tmp_files[path],'r') as f:
                f.seek(offset)
                data = f.read(size)
            return  data

        #Get data from the chunks
        else:
            self.req_cnt = self.req_cnt + 1
            db = chunk_database()
            #get the complete chunks list for the file
            chunks_list = get_chunk_list(db,path[1:],offset,size)
            data = get_chunks_data(chunks_list,offset,size)
            db.close()
            # print(data)
            return data
        # with self.rwlock:
        #     os.lseek(fh, offset, 0)
        #     return os.read(fh, size)



    def readdir(self, path, fh):
        self.req_cnt = self.req_cnt + 1
        req = request_dir_info(self.req_cnt, path)
        resp = self.stub.GetResponse(req)
        files = [f.filename for f in resp.filesinfo] #Extract just the file names from the array
        return ['.', '..'] + files

    readlink = os.readlink



    #TODO: Clear off the file entries from the table
    def release(self, path, fh):
        db = chunk_database()


        if path in self.tmp_files:
            filenm = self.tmp_files[path]

            # creates chunks and adds to DB.
            splice_file(db, filenm, pseudofilenm=path, write_to_chunkfile=True)

            #Use the written chunks data while calling write chunk data
            self.reqid = self.reqid + 1

            # Get the Storage Server's details for wrting the data
            req = request_write_chunk(self.reqid,path)
            resp = self.stub.GetResponse(req)

            #Send all teh chunk data associated with the file to a storage server
            push_chunks_to_storage_server(resp,path)

            del self.tmp_files[path]

        db.delete_chunks_for_file(path)
        return 0
        # return os.close(fh)

    def rename(self, old, new):
        return os.rename(old, self.root + new)

    rmdir = os.rmdir

    def statfs(self, path):
        stv = os.statvfs(path)
        ret_val = dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                                                         'f_frsize', 'f_namemax'))
        ret_val['f_bsize'] = 1
        return ret_val

    def symlink(self, target, source):
        return os.symlink(source, target)

    def truncate(self, path, length, fh=None):
        with open(path, 'r+') as f:
            f.truncate(length)

    unlink = os.unlink
    utimens = os.utime

    def write(self, path, data, offset, fh):
        if path in self.tmp_files:
            with open(self.tmp_files,'w') as f:
                f.seek(offset)
                f.write(data)
        return len(data)
        # with self.rwlock:
        #     os.lseek(fh, offset, 0)
        #     return os.write(fh, data)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    root = "."
    mount = "/tmp/fuse2/"
    fuse = FUSE(Loopback(root), mount, foreground=True)
