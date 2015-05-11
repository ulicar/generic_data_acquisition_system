# Generic Data Acquisition System

GDAS consists of several subsystems:
* Wizard    - microservice for collecting (receiving) data from outside sources called Cores
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
