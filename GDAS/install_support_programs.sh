#!/bin/bash

# Script for installing support programs: UWSGI, PYTHON, NGINX, ...

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

PYTHON=python2.7
UWSGI=uwsgi
NGINX=nginx
SUPERVISOR=supervisor
HAPROXY=haproxy

declare -a programs=(PYTHON UWSGI NGINX SUPERVISOR HAPROXY)

apt-get install ${programs[@]}
