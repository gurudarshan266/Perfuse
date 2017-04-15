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
        hash, filename, offset, length)
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
        sql_query = "DELETE FROM CHUNKS WHERE FILENAME='%s';" % filenm
        try:
            self.cur.execute(sql_query)
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
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def is_incache(self,hash,val=True):
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


    def close(self):
        self.con.close()

# init_db()
# mydb = chunk_database("/home/guru/esa_project/Client/tt.db")
# mydb.create_table()
# print(mydb.get_all_rows())
# mydb.add_chunk("hello","a.txt",0,10)
# print(mydb.get_all_rows())
# mydb.close()
