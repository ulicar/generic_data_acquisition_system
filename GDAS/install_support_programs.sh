#!/bin/bash

# Script for installing support programs: UWSGI, PYTHON, NGINX, ...

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

PYTHON=python2.7 python-dev
UWSGI=uwsgi
NGINX=nginx
SUPERVISOR=supervisor
HAPROXY=haproxy
PIP=python-pip
MONGO=mongodb
RABBIT=rabbitmq-server

declare -a programs=($PYTHON $UWSGI $NGINX $SUPERVISOR $HAPROXY $PIP $MONGO $RABBIT)

apt-get install ${programs[@]}


