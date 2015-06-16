# Generic Data Acquisition System

GDAS consists of several subsystems:
* Wizard    - microservice for collecting (receiving) data from outside sources called Cores
* Apprentice- microservice for collecting (asking for) data from outside sources called Cores
* Pigeon    - microservice used for sorting data by type and Core id
* Worker    - microservice used for saving data to database called Fatty
* Fatty     - wrapper library around python-pymongo and MongoDB
* Rabbit    - wrapper library around python-pika and RabbitMQ
* GDAS Util - utility library for GDAS:
  * communication  - Publisher and Consumer for Rabbit
  * database       - Fatty
  * input          - argument parser
  * security       - authentication library for GDAS

  * other :
    * setup_rabbit  - creates some default queues on Rabbit
    * create_user   - helper script for user creating in Fatty
* Other: configuration files


# Supervisor

  Enable Web interface /etc/supervisor/supervisor.conf
  [inet_http_server]
  port = 127.0.0.1:9001
  username = Supervisor
  password = StrongPassword

  Starting supervisor: service supervisor start
  Gdas configuration file: /etc/supervisor/conf.d/gdas.supervisor.ini.default.conf

  Controlling services:
  GROUPNAMES are wizads, pigeons, workers, hobbits, cores
  supervisorctl start GROUPNAME:*

  or

  supervisorctl start PROGRAM:PROGRAM_NUMBER



# MongoDB

  Enable web interface /etc/mongod.conf (Port is set to: 27017 + 1000 = 28017)
  httpinterface = true
  rest = true

  use command 'mongo' to start interactive shell

  or use GDAS-MongoDB interface to see saved data


# Nginx

  Configuration in /etc/nginx/sites-enabled/gdas.nginx.ini.default
  Maps hostname and url to our flask apps (to uwsgi socket)


# Uwsgi

  Starts flask apps, web interface is disabled on default (see PROGRAM.uwsgi.ini.default to enable)

# Possible errors:
1) Wizard cannot mount app "cannot load python-eggs"
   mkdir -p /home/gdas/.python-eggs
   chown gdas:gdas /home/gdas/.python-eggs
   mkdir /tmp/python-eggs
   export PYTHON_EGG_CACHE=/tmp/python-eggs
   
2) Wizard permission error on log file
   sudo chown -r gdas:gdas /opt/gdas/ 
   
1-2) If query: http://victim.no-ip.org:8080/api/wizard/upload passes, bugs are fixed.   

   