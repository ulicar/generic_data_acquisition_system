#!/bin/bash

# Script for installing GDAS user

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

GDASUSER=gdas

adduser $GDASUSER --no-create-home --system --group
