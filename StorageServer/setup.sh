#!/bin/sh

apt-get install python-pip python-dev build-essential
apt-get install python-virtualenv

#Create the chunks directory
if [ ! -d "chunks" ]; then
    mkdir chunks/
fi

if [ ! -d "venv" ]; then
    apt-get install python-pip python-dev build-essential 
    python -m pip install --upgrade pip
    python -m pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    python -m pip install --upgrade pip
fi

apt-get install sqlite3


python -m pip install grpcio
python -m pip install grpcio-tools
python -m pip install pyping pika

# Location packages
python -m pip install python-geoip python-geoip-geolite2
python -m pip install requests


mkdir ../Common/MsgTemplate/PyTemplate
make -C ../Common/MsgTemplate
