#!/bin/bash

# Script for installing support programs: UWSGI, PYTHON, NGINX, ...

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

PYTHON=python2.7 
DEV=python-dev
BUILD=build-essential
UWSGI=uwsgi
UWSGI_PLUG=uwsgi-plugin-python
NGINX=nginx
SUPERVISOR=supervisor
HAPROXY=haproxy
PIP=python-pip
MONGO=mongodb
RABBIT=rabbitmq-server

declare -a programs=($PYTHON $DEV $BUILD $UWSGI $UWSGI_PLUG $NGINX $SUPERVISOR $HAPROXY $PIP $MONGO $RABBIT)

apt-get install ${programs[@]}


