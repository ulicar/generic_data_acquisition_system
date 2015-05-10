#!/bin/bash

echo 'Stopping. Script not yet tested'
exit -1:

# Setup script for GDAS system

PYTHON=$(which python2.7)
UWSGI=$(which uwsgi)
NGINX=$(which nginx)


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
    echo 'sudo apt-get install python' && exit -1
else
    echo -e 'python installed.\n'
fi

if [ ! -f $UWSGI ]; then
    echo 'sudo apt-get install uwsgi' && exit -1
else
    echo -e 'uwsgi installed.\n'
fi

if [ ! -f $NGINX ]; then
    echo 'sudo apt-get install nginx' && exit -1
else
    echo -e 'nginx installed.\n'
fi

# Test prerequisites
python -c 'import setuptools' 2>/dev/null
[ $? == 1 ] && echo -e '[REQUIRED] Install python2.7 setuptools\n' &&

# Install subsystems
echo -e 'Starting installation...\n'

#Creating User
for package in ${array[*]}
do
    adduser gdas --no-create-home --system --group
    echo -e "Created gdas user.\n"
done

# Install packages
for package in ${array[*]}
do
    cd ${GDAS}${package}
    $PYTHON setup.py install 2>/dev/null
    echo -e 'Installed ${package} package. \n'
done

cp /etc/gdas/wizard/message_collector.nginx.ini.default /etc/nginx/sites-available/.
ln -s /etc/nginx/sites-available/message_collector.nginx.ini.default /etc/nginx/sites-enabled/message_collector.nginx.ini.default

ln -s /etc/gdas/wizard/message_collector.conf /etc/init/gdas-wizard.conf
