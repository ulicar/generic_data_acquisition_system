#!/bin/bash

# Script for installing GDAS subsystems

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

# All GDAS subsystems
TOP=$(pwd)
APPRENTICE=apprentice
PIGEON=pigeon
WIZARD=wizard
WORKER=worker
UTILS=util
CORES=tests/mocking/cores

declare -a DIRS=($UTILS $APPRENTICE $PIGEON $CORES $WIZARD $WORKER)

for dir in ${DIRS[@]}; do
    if [ -d $dir ]; then
        cd $dir
        /usr/bin/python setup.py install >/dev/null 2>&1 || exit -1
        echo "Installed $dir"
        rm -rf *egg* *.pyc *build* *dist*
        cd $TOP
    else
        echo "Missing $dir"
    fi
done

echo 'Setting up Rabbit queues' && cd $UTILS
/usr/bin/python setup_rabbit.py

echo 'Rabbit set up.'
