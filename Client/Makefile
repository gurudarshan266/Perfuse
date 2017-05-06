setup:
	sh setup.sh

setupdb:
	sh setupdb.sh

cleandb:
	rm files.db

clean:
	sqlite3 files.db < cleandb.sql
	rm chunks/*
	rm tmp/*
	sqlite3 files.db < seed.sql
