setup:
	sh setup.sh

setupdb:
	sh setupdb.sh

cleandb:
	rm chunks.db

clean:
	sqlite3 chunks.db < cleandb.sql
	rm chunks/*
	sqlite3 chunks.db < seed.sql
