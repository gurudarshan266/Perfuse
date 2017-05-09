#!/bin/sh


if [ ! -d "fusepy" ]; then
    git clone https://github.com/terencehonles/fusepy
    touch fusepy/__init__.py
fi

#Create the chunks directory
if [ ! -d "chunks" ]; then
    mkdir chunks/ 
    mkdir tmp/
fi

apt-get install python-pip python-dev build-essential
apt-get install python-virtualenv

if [ ! -d "venv" ]; then
    python -m pip install --upgrade pip
    python -m pip install virtualenv
    virtualenv venv
    source venv/bin/activate
fi


python -m pip install --upgrade pip
python -m pip install grpcio
python -m pip install grpcio-tools

# RabbitMQ tools
python -m pip install pika

# Ping
python -m pip install pyping

# Location packages
python -m pip install python-geoip python-geoip-geolite2
python -m pip install requests

mkdir ../Common/MsgTemplate/PyTemplate
make -C ../Common/MsgTemplate
