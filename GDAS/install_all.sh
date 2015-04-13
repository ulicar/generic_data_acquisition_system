#!/bin/bash

# Setup script for GDAS system

PYTHON=/usr/bin/python2.6
GDAS=$(pwd)
HOBBIT=hobbit
PIGEON=pigeon
UTIL=util
TESTS=tests
WIZARD=wizard
WORKER=worker

PACKAGES={$UTIL $HOBBIT $WORKER $WIZARD $PIGEON}

[ -d $HOBBIT ] || echo "$HOBBIT directory missing. Are you in GDAS directory? " || exit -1
[ -d $PIGEON ] || echo "$PIGEON directory missing" || exit -1
[ -d $UTIL   ] || echo "$UTIL   directory missing" || exit -1
[ -d $TESTS  ] || echo "$TESTS  directory missing" || exit -1
[ -d $WIZARD ] || echo "$WIZARD directory missing" || exit -1
[ -d $WORKER ] || echo "$WORKER directory missing" || exit -1

if [ ! -f $PYTHON ]; then
    echo 'sudo apt-get install python2.6' && exit -1
fi

# Test prerequisites
python -c 'import setuptools' 2>/dev/null
[ $? == 1 ] && echo '[REQUIRED] Install python2.6 setuptools' && exit -1

# Install subsystems
echo -e 'Starting installation...\n'

# Creating Users
for package in ${array[*]}
do
    adduser gdas_${package} -g gdas
    echo -e "Created gdas_${package} user.\n"
done

# Install packages
for package in ${array[*]}
do
    cd ${GDAS}${package}
    $PYTHON setup.py install 2>/dev/null
    echo -e 'Installed ${package} package. \n'
done

