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
rabbitmqctl add_user gdas GgdasS
rabbitmqctl set_user_tags gdas administrator
rabbitmqctl set_permissions -p / gdas ".*" ".*" ".*"
rabbitmq-plugins enable rabbitmq_management
/usr/bin/python setup_rabbit.py

service rabbitmq-server restart

echo 'Rabbit set up.'

#Add ADMIN account to mongodb (gdas/gdas)
echo 'Setting up Mongodb'

mongo gdas <<EOF
db.accounts.insert({'username':'gdas', "password" : "1e6887a950fd3d6910c8230156e6536d58377a611e6887a950fd3d6910c8230156e6536d58377a61", "description" : "GDAS admin user account", "roles" : [ "admin/manage" , "admin/read" , "admin/admin" , "admin/upload"]})
db.accounts.insert({'username':'jdomsic', "password" : "3fd23c5146f6e075b7cb06cd0766a5b7de8eb49b3fd23c5146f6e075b7cb06cd0766a5b7de8eb49b", "description" : "jdomsic user account", "roles" : [ "basic/upload" , "wizard/upload" , "basic/read" , ""]})

EOF


