# Perfuse
There are 3 parts to the code:
1) Chunk Server
2) Storage Server
3) Client

Chunk Server is written in Java. Client and Storage Server are written using Python.

The Client uses Python FUSE library from https://github.com/terencehonles/fusepy

To run Chunk Server, please ensure that MySQL and Maven are installed

To run Client and Storage server, run "source setup.sh" in their respective directories with root privileges.

Use "make clean" for Storage Server and Client to remove any chunks from the local cache. 

Root privileges are mandatory for the Storage Server because PyPing module uses ICMP libraries to create ping packets which cannot be accessed without root access.

Mount point for the Client FUSE file system is: /tmp/fuse2

Replication Factor and the Client IP must be set in Client/constants.py file

Storage Server IP must be set in StorageServer/constants.py file

To run Client use:
python fusefs.py <IP address of chunk server>

To run Storage Server use:
python storage_server.py <IP address of chunk server>


