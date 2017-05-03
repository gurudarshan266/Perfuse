#!/usr/bin/python

import sqlite3


class chunk_database:
    def __init__(self, name="files.db"):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
            # self.create_table()

    def create_table(self):
        sql_query = "CREATE TABLE CHUNKS (" \
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "HASH VARCHAR(40) NOT NULL," \
                    "FILENAME VARCHAR(255) NOT NULL," \
                    "OFFSET INT NOT NULL," \
                    "LEN INT NOT NULL,"\
                    "INCACHE INTEGER DEFAULT 0,"\
                    "SSIP VARCHAR(15)," \
                    "SSPORT INTEGER DEFAULT 50004);"
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def add_chunk(self, hash, filename, offset, length, ssip, ssport):
        sql_query = "INSERT INTO CHUNKS (HASH,FILENAME,OFFSET,LEN,SSIP,SSPORT) VALUES ('%s','%s',%d,%d,'%s',%d);" % (
        hash, filename, offset, length,ssip,ssport)
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def is_chunk_present(self, hash):
        sql_query = "SELECT * FROM CHUNKS WHERE HASH='%s';" % hash
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        return len(self.cur.fetchall()) > 0

    def get_chunks_for_file(self, filenm):
        sql_query = "SELECT * FROM CHUNKS WHERE FILENAME='%s';" % filenm
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        rows = self.cur.fetchall()[:]
        return rows

    def delete_chunks_for_file(self, filenm):
        print "Deleting %s hashes from DB"%filenm
        sql_query = "DELETE FROM CHUNKS WHERE FILENAME='%s';" % filenm
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def get_all_rows(self):
        sql_query = "SELECT * FROM CHUNKS;"
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        rows = self.cur.fetchall()
        return rows

    def set_incache(self,hash,val=True):
        value = 1 if val else 0
        sql_query = "UPDATE CHUNKS SET INCACHE=%d WHERE HASH='%s';"%(value,hash)
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def is_incache(self,hash):
        sql_query = "SELECT INCACHE FROM CHUNKS WHERE HASH='%s';"%hash
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        rows = self.cur.fetchall()
        if len(rows)==0:
            return False
        val = rows[0][0]
        return True if val==1 else False

    def update_offsets(self,filenm,start,delta):
        sql_query = "UPDATE CHUNKS SET OFFSET = OFFSET + %d WHERE FILENAME = '%s' AND OFFSET > %d;" % (delta, filenm,start)
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def remove_hashes_after_offset(self,filenm,offset):
        sql_query = "DELETE FROM CHUNKS WHERE FILENAME='%s' AND OFFSET>%d;" % (filenm,offset)
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def update_hash(self,filenm,hash,id,size):
        sql_query = "UPDATE CHUNKS SET HASH = '%s', LEN = %d WHERE ID = %d AND FILENAME = '%s';" % (hash,size,id,filenm)
        try:
            self.cur.execute(sql_query)
            self.con.commit()
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def get_file_size(self,filenm):
        sql_query = "SELECT SUM(LEN) FROM CHUNKS WHERE FILENAME='%s';"%filenm
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        rows = self.cur.fetchall()
        if len(rows)==0:
            return 0
        val = rows[0][0]
        return val



    def close(self):
        self.con.close()

# init_db()
# mydb = chunk_database()
# mydb.create_table()
# print(mydb.get_all_rows())
# print(mydb.get_all_rows())
# mydb.close()

# mydb.add_chunk("hello","a.txt",0,10,"127.0.0.1",50004)
# print(mydb.get_file_size("a.txt"))
