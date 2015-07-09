#!/bin/bash

# Script for installing gdas

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

ufw allow ssh
ufw enable

echo 'Step 1: Install support.'
./install_support_programs.sh    || exit -1

echo 'Step 2: Install python modules.'
./install_python_modules.sh

echo 'Step 3: Install GDAS.'
./install_gdas_subsystems.sh

echo 'Step 4: Create user.'
./install_gdas_user.sh

echo 'Step 5: Housekeeping.'
./post_install.sh                || exit -1
cp README.md /opt/gdas/
chown -R gdas:gdas /opt/gdas

echo 'Step 6: 100% DONE!.'



