#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging
import sys
import os
import ntpath

sys.path.append(os.path.abspath("../Common/MsgTemplate/PyTemplate"))

from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock
from stat import *
from shutil import copyfile

# from fusepy.fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from fusepy.fuse import *
from requestpb_utils import *
from responsepb_utils import *
import constants
import chunkserver_pb2_grpc
from db_utils import *
from file_splicer_utils import *

class Loopback(LoggingMixIn, Operations):
    def __init__(self, root):
        # self.root = realpath(root)
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
        tmp_filenm = TMP_DIR+"file"+str(self.tmpfiles_id)
        self.tmpfiles_id = self.tmpfiles_id + 1
        self.tmp_files[path] = tmp_filenm
        f=open(tmp_filenm,'w+')
        f.close()
        return 4#self.tmpfiles_id

        #return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)

    #TODO: Need to splice the files at this stage while writing
    def flush(self, path, fh):
        return 0
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        return 0
        if datasync != 0:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def getattr(self, path, fh=None):
        print("In get attr")
        if(path=="/.Trash" or path=="/.Trash-1000"):
            raise FuseOSError(EACCES)

        if path in self.tmp_files:
            st = os.lstat(self.tmp_files[path])
            attr = dict((key, getattr(st, key)) for key in
                        ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
            return attr

        self.req_cnt = self.req_cnt + 1

        uid,gid,pid = fuse_get_context()

        req = request_file_info(self.req_cnt, path)
        resp = self.stub.GetResponse(req)
        # print(resp)

        # return the error code if any
        if resp.ec < 0:
            raise FuseOSError(-1*resp.ec)

        # attr = dict()float(file.lastmodified)#to be changed
        st = os.lstat("scaffold/")
        attr =  dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime','st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        # return attr

        if(len(resp.filesinfo)>0):
            file = resp.filesinfo[0]  # Only the first entry is required
            attr['st_mtime'] = to_epoch(file.lastmodified)#file.lastmodified
            attr['st_ctime'] = to_epoch(file.lastmodified)#file.lastmodified#to be changed
            attr['st_atime'] = to_epoch(file.lastmodified)#file.lastmodified#to be changed
            attr['st_size'] = file.size
            attr['st_mode'] = 0755 | (S_IFREG if not file.is_dir else S_IFDIR)
            attr['st_nlink'] = 2
            attr['st_dev'] = 0
            attr['st_blksize'] = 4096
            attr['st_blocks'] = 0
            attr['st_gid'] = gid
            attr['st_uid'] = uid
        return attr

    getxattr = None

    def link(self, target, source):
        return os.link(source, target)

    listxattr = None
    # mkdir = os.mkdir
    mknod = os.mknod
    #open = os.open

    def mkdir(self, path, mode):
        self.req_cnt = self.req_cnt + 1
        req = request_add_dir(self.req_cnt,path)
        resp = self.stub.GetResponse(req)
        print(resp)
        return resp.ec


    def open(self, file, mode):
        self.req_cnt = self.req_cnt + 1
        # return 5
        req = request_file_hashes(self.req_cnt,file)
        print(req)
        resp = self.stub.GetResponse(req)
        print(resp)
        db = chunk_database()
        add_file_hashes_to_db(db,resp)
        return 4



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
            #TODO: check why path[1:] is present
            chunks_list = get_chunk_list(db,path,offset,size)
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
        print(resp)

        # basename is required because read dir expects just the file name not the complete path
        files = [ntpath.basename(f.filename) for f in resp.filesinfo] #Extract just the file names from the array
        return ['.', '..'] + files

    readlink = os.readlink



    def release(self, path, fh):
        db = chunk_database()

        if path in self.tmp_files:
            filenm = self.tmp_files[path]

            # creates chunks and adds to DB.
            splice_file(db, filenm, pseudofilenm=path, write_to_chunkfile=True)

            # Use the written chunks data while calling write chunk data
            self.req_cnt = self.req_cnt + 1

            # Get the Storage Server's details for writing the data
            req = request_write_chunk(self.req_cnt,path)
            resp = self.stub.GetResponse(req)

            # Send all the chunk data associated with the file to a storage server
            push_chunks_to_storage_server(resp,path)

            # Send update to chunkserver about file info change
            self.req_cnt = self.req_cnt + 1
            st = os.lstat(self.tmp_files[path])
            mtime = to_utc(st.st_mtime)
            req2 = request_update_fileinfo(self.req_cnt,path,st.st_size,mtime,S_ISDIR(st.st_mode))
            resp2 = self.stub.GetResponse(req2)

            del self.tmp_files[path]

        else:
            # Send request to remove the file on chunk server
            self.req_cnt += 1
            r2 = request_remove_file(self.req_cnt, path, is_dir=False)
            resp2 = self.stub.GetResponse(r2)

            # Get the Storage Server's details for writing the data
            self.req_cnt = self.req_cnt + 1
            req = request_write_chunk(self.req_cnt, path)
            resp = self.stub.GetResponse(req)

            # Send all the chunk data associated with the file to a storage server
            push_chunks_to_storage_server(resp, path)

            # Send update to chunkserver about file info change
            self.req_cnt += 1
            sz = db.get_file_size(path)
            mtime = datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            req2 = request_update_fileinfo(self.req_cnt, path, sz, mtime, is_dir=False)
            resp2 = self.stub.GetResponse(req2)


        # Clear off the hash entries of the file from the table
        db.delete_chunks_for_file(path)
        return 0
        # return os.close(fh)

    # TODO: use update file info to rename a file
    def rename(self, old, new):
        return os.rename(old, self.root + new)

    def rmdir(self, path):
        self.req_cnt += 1
        r=request_remove_file(self.req_cnt,path, True)
        resp = self.stub.GetResponse(r)
        print(resp)
        return resp.ec


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
        #If its a temporary file, truncate the tmp file
        if path in self.tmp_files:
            with open(self.tmp_files[path], 'r+') as f:
                f.truncate(length)
            return 0

        else:
            # return 0
            # Get the file info to know if the given length is smaller or larger than the file
            self.req_cnt += 1
            r = request_file_info()
            resp = self.stub.GetResponse(r)

            # If the file is not found raise appropriate errno
            if resp.ec < 0:
                raise FuseOSError(-1*resp.ec)

            fileinfo = resp.filesinfo[0]
            db = chunk_database()

            # if the new length is same as old length,
            # return without proceeding forward
            if length == fileinfo.size:
                return 0

            elif length<fileinfo.size:
                #get the row corresponding to the truncation length
                c = get_chunk_list(db,path,length,0)[0]

                #Remove the hashes after the new length
                db.remove_hashes_after_offset(path,length)

                #Download the chunk data if already not present
                get_chunk_data(hash=c[HASH_INDEX],offset=c[OFFSET_INDEX],len=0,
                               ssip=c[SSIP_INDEX],ssport=c[SSPORT_INDEX],filenm=path)

                # Copy the contents of the chunk file into a new file
                new_chunknm = CHUNKS_DIR + c[HASH_INDEX] + ".cp"
                copyfile(new_chunknm, CHUNKS_DIR + c[HASH_INDEX])

                # Truncate the chunk file
                newhash=""
                with open(new_chunknm,"r+") as f:
                    new_len = length-c[OFFSET_INDEX]
                    # Truncate the chunk
                    f.truncate(new_len)
                    data = f.read()
                    # Compute the new hash
                    newhash = compute_hash(data)
                    # Upodate the hash in the table
                    db.update_hash(path,newhash,c[ID_INDEX], new_len)

                # Rename the chunk file name to match its hash
                os.rename(new_chunknm,CHUNKS_DIR+newhash)
                new_chunknm = CHUNKS_DIR+newhash

            #TODO: if length > fileinfo.size

            # Send request to remove the file on chunk server
            self.req_cnt += 1
            r2 = request_remove_file(self.req_cnt, path, is_dir=False)
            resp2 = self.stub.GetResponse(r2)

            # Get the Storage Server's details for writing the data
            self.req_cnt = self.req_cnt + 1
            req = request_write_chunk(self.req_cnt, path)
            resp = self.stub.GetResponse(req)

            # Send all the chunk data associated with the file to a storage server
            push_chunks_to_storage_server(resp, path)

            # Send update to chunkserver about file info change
            self.req_cnt += 1
            st = os.lstat(new_chunknm)
            mtime = to_utc(st.st_mtime)
            req2 = request_update_fileinfo(self.req_cnt, path, length, mtime, S_ISDIR(st.st_mode))
            resp2 = self.stub.GetResponse(req2)

            return 0








    # unlink = os.unlink
    def unlink(self, path):
        self.req_cnt = self.req_cnt + 1
        r = request_remove_file(self.req_cnt,path,False)
        print(r)
        resp = self.stub.GetResponse(r)
        print(resp)
        return resp.ec


    utimens = os.utime

    # TODO: take care of append test cases
    def write(self, path, data, offset, fh):

        # If the file is newly created, directly write to the file
        if path in self.tmp_files:
            with open(self.tmp_files[path],'w') as f:
                f.seek(offset)
                f.write(data)

        # If not in newly created, search in local cache or download from Storage Server
        else:
            db = chunk_database()
            file_sz = db.get_file_size(path)


            # Get the row corresponding to the offset
            # len=0 so that no data is returned. Just used for downloading
            if offset < file_sz:
                chunk_row = get_chunk_list(db, path, offset, 0)[0]
                hash = chunk_row[HASH_INDEX]

            # For append cases, always add data to the last chunk
            else:
                modified_offset = offset -1
                chunk_row = get_chunk_list(db, path, modified_offset, 0)[0]
                hash = chunk_row[HASH_INDEX]
                print("Appending to file %s"%path)

            # If the chunk is not in cache, download the chunk file to local cache
            if chunk_row[INCACHE_INDEX]==0:
                get_chunk_data(hash,0,0,chunk_row[SSIP_INDEX],chunk_row[SSPORT_INDEX])

            # Copy the contents of the chunk file into a new chunk file
            new_chunknm = CHUNKS_DIR + chunk_row[HASH_INDEX] + ".cp"
            copyfile(new_chunknm, CHUNKS_DIR + chunk_row[HASH_INDEX])

            # Write data to the copied chunk file
            newhash = ""
            data=""
            with open(new_chunknm,'w') as f:
                offset_in_chunk = offset - chunk_row[OFFSET_INDEX]
                f.seek(offset_in_chunk)
                f.write(data)
                data2 = f.read()
                # Compute the new hash
                newhash = compute_hash(data2)
                # Update the hash in the table
                st = os.lstat(new_chunknm)
                new_chunk_len = st.st_size
                db.update_hash(path, newhash, chunk_row[ID_INDEX], len(data2))

            # Rename the chunk file name to match its hash
            os.rename(new_chunknm, CHUNKS_DIR + newhash)
            new_chunknm = CHUNKS_DIR + newhash

            #TODO: Send invalidation message to chunk server

            # Update offsets of the chunk hashes following it
            db.update_offsets(path,chunk_row[OFFSET_INDEX],delta=len(data))



        return len(data)
        # with self.rwlock:
        #     os.lseek(fh, offset, 0)
        #     return os.write(fh, data)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    root = "."
    mount = "/tmp/fuse2/"
    fuse = FUSE(Loopback(root), mount, foreground=True)
