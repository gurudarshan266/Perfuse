#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock

import os

from fusepy.fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from requestpb_utils import *
from responsepb_utils import *
import constants
import chunkserver_pb2_grpc
from db_utils import *

class Loopback(LoggingMixIn, Operations):
    def __init__(self, root):
        self.root = realpath(root)
        self.rwlock = Lock()

        self.req_cnt = 0

        #Connect to server
        self.channel = grpc.insecure_channel(constants.CHUNK_SERVER_IP+":"+str(constants.CHUNK_SERVER_PORT))
        self.stub = chunkserver_pb2_grpc.ChunkServerStub(self.channel)

        self.db = chunk_database()

    def __call__(self, op, path, *args):
        return super(Loopback, self).__call__(op, self.root + path, *args)

    def access(self, path, mode):
        if not os.access(path, mode):
            raise FuseOSError(EACCES)

    chmod = os.chmod
    chown = os.chown

    def create(self, path, mode):
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)

    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        if datasync != 0:
          return os.fdatasync(fh)
        else:
          return os.fsync(fh)

    def getattr(self, path, fh=None):
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    getxattr = None

    def link(self, target, source):
        return os.link(source, target)

    listxattr = None
    mkdir = os.mkdir
    mknod = os.mknod
    #open = os.open

    def open(self, file, flags, mode):
        self.req_cnt = self.req_cnt + 1
        req = request_file_hashes(self.req_cnt,file)
        print(req)
        resp = self.stub.GetResponse(req)
        print(resp)
        add_file_hashes_to_db(self.db,resp)

    def read(self, path, size, offset, fh):
        with self.rwlock:
            os.lseek(fh, offset, 0)
            return os.read(fh, size)

    def readdir(self, path, fh):
        return ['.', '..'] + os.listdir(path)

    readlink = os.readlink

    def release(self, path, fh):
        return os.close(fh)

    def rename(self, old, new):
        return os.rename(old, self.root + new)

    rmdir = os.rmdir

    def statfs(self, path):
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def symlink(self, target, source):
        return os.symlink(source, target)

    def truncate(self, path, length, fh=None):
        with open(path, 'r+') as f:
            f.truncate(length)

    unlink = os.unlink
    utimens = os.utime

    def write(self, path, data, offset, fh):
        with self.rwlock:
            os.lseek(fh, offset, 0)
            return os.write(fh, data)


if __name__ == '__main__':
    if len(argv) != 3:
        print('usage: %s <root> <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(Loopback(argv[1]), argv[2], foreground=True)
