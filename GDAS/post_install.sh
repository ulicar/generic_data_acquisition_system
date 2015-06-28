#!/bin/bash

# Script for doing some post-install work: changing ownerships, etc.

if [ ! $USER == 'root' ]; then
    echo 'Must be superuser' && exit -1
fi

# Create some folders
mkdir /opt/gdas/var/log -p

# Change ownership of GDAS
chown -R gdas:gdas /opt/gdas/
chown -R gdas:gdas /etc/gdas/
echo 'Changing ownership of files.'

# Copy GDAS configuration files
NGINX_CONF=gdas.nginx.ini.default
SUPER_CONF=gdas.supervisor.ini.default
HAPROXY_CONF=haproxy.cfg

declare -a FILES=($NGINX_CONF $SUPER_CONF $HAPROXY_CONF)
for conf in ${FILES[@]}; do
    if [ ! -f $conf ]; then
        echo "$conf file missing."
        exit -1
    fi
done

echo 'Moving config files to appropriate locations.'

cp "$NGINX_CONF" /etc/nginx/sites-available/.
ln -fs /etc/nginx/sites-available/"$NGINX_CONF" /etc/nginx/sites-enabled/"$NGINX_CONF"

cp "$SUPER_CONF" /etc/supervisor/conf.d/"$SUPER_CONF".conf

mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.old
cp "$HAPROXY_CONF" /etc/haproxy/haproxy.cfg

# Add web interface for Supervisor
cat >> /etc/supervisor/supervisor.conf << EOF

[inet_http_server]
port=9001
username=gdas
password=gdas

EOF

# Open ports
echo 'Open ports for GDAS'

ufw allow 5672  # rabbitMq ampq
ufw allow 15672 # rabbitMq web interface
ufw allow 27018 # mongo port
ufw allow 28014 # mongo web interface
ufw allow 9001  # supervisor
ufw allow 9030  # Santa uwsgi
ufw allow 9020  # Wizard uwsgi
ufw allow 9010  # mocking cores uwsgi
ufw allow 8080  # nginx
ufw allow 80    # HAproxy

#Reaload services
supervisorctl reload
service supervisor start
supervisorctl start cores:*

rm /etc/nginx/sites-enabled/default
service ngnix reload
service haproxy reload

echo 'Done.'
