#!/bin/bash

# Script for installing support python packages

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

declare -a PACKAGES=('setuptools' 'flask==0.10.1' 'uwsgi' 'validictory' 'pymongo==3.0' 'pika==0.9.14' 'requests' 'mock')
pip install ${PACKAGES[@]}
