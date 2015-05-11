#!/bin/bash

# Script for installing GDAS subsystems

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

# All GDAS subsystems
TOP=$(pwd)
HOBBIT=hobbit
PIGEON=pigeon
WIZARD=wizard
WORKER=worker
UTILS=util
CORES=tests/mocking/cores

declare -a DIRS=($UTILS $HOBBIT $PIGEON $CORES $WIZARD $WORKER)

for dir in ${DIRS[@]}; do
    if [ -d $dir ]; then
        cd $dir
        /usr/bin/python setup.py install >/dev/null 2>&1 || exit -1
        echo "Installed $dir"
        cd $TOP
    else
        echo "Missing $dir"
    fi
done
