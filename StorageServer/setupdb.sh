#!/bin/sh

apt-get install sqlite3
touch chunks.db
sqlite3 chunks.db << EOF
CREATE TABLE CHUNKS (ID INTEGER PRIMARY KEY AUTOINCREMENT, HASH VARCHAR(40) NOT NULL, LEN INT NOT NULL);
EOF