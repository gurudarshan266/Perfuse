#!/bin/sh

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