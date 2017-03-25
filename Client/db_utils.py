import sqlite3

con = None
cur = None

def create_table():
    sql_query = "CREATE TABLE CHUNKS (" \
        "ID INTEGER PRIMARY KEY AUTOINCREMENT,"\
        "HASH VARCHAR(40) NOT NULL,"\
        "FILENAME VARCHAR(255) NOT NULL,"\
        "OFFSET INT NOT NULL,"\
        "LEN INT NOT NULL);"
    try:
        cur.execute(sql_query)
    except sqlite3.Error, e:
        print "Error : %s"% e.args[0]

def add_chunk(  hash, filename, offset, length):
    sql_query = "INSERT INTO CHUNKS (HASH,FILENAME,OFFSET,LEN) VALUES ('%s','%s',%d,%d);"%(hash,filename,offset,length)
    cur.execute(sql_query)

def is_chunk_present( hash):
    cur = con.cursor()
    sql_query = "SELECT * FROM CHUNKS WHERE HASH='%s';" % hash
    cur.execute(sql_query)
    return len(cur.fetchall())>0

def init_db():
    con = sqlite3.connect("files.db")

    with con:
        cur = con.cursor()
        return cur

init_db()
create_table()
add_chunk("adas","a.txt",0,10)
print(is_chunk_present("adas"))