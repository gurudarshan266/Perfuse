CREATE TABLE CHUNKS ( 
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    HASH VARCHAR(40) NOT NULL, 
                    FILENAME VARCHAR(255) NOT NULL, 
                    OFFSET INT NOT NULL, 
                    LEN INT NOT NULL,
                    INCACHE INTEGER DEFAULT 0,
                    SSIP VARCHAR(15),
                    SSPORT INTEGER DEFAULT 50004);
