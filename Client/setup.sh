#!/bin/sh

if [ ! -d "fusepy" ]; then
    git clone https://github.com/terencehonles/fusepy
    touch fusepy/__init__.py
fi

#Create the chunks directory
if [ ! -d "chunks" ]; then
    mkdir chunks/
fi

if [ ! -d "venv" ]; then
    python -m pip install --upgrade pip
    python -m pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install grpcio
    python -m pip install grpcio-tools
fi
