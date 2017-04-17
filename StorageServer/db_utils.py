import sqlite3

class chunk_database:
    def __init__(self, name="chunks.db"):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
            # self.create_table()

    def create_table(self):
        sql_query = "CREATE TABLE CHUNKS (" \
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "HASH VARCHAR(40) NOT NULL," \
                    "LEN INT NOT NULL);"
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]

    def add_chunk(self, hash, length):
        sql_query = "INSERT INTO CHUNKS (HASH,LEN) VALUES ('%s',%d);" % (
        hash, length)
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

    def get_total_size(self):
        sql_query = "SELECT SUM(LEN) FROM CHUNKS;"
        try:
            self.cur.execute(sql_query)
        except sqlite3.Error, e:
            print "Error : %s" % e.args[0]
        rows = self.cur.fetchone()
        if len(rows) == 0:
            return 0
        return rows[0]

    def close(self):
        self.con.close()

    def __del__(self):
        self.con.close()

# init_db()
# mydb = chunk_database("chunks.db")
# mydb.create_table()
# print(mydb.get_all_rows())
# mydb.add_chunk("hello","a.txt",0,10)
# print(mydb.get_all_rows())
# mydb.close()
