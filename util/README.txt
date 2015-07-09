Utility package.
Consists of communication, database, input and security packages.

Communication:
    RabbitMQ (pika framework) publisher and subscriber modules.

Database:
    API for working with Fatty (MongoDB and pymongo)

Input:
    Argument parser for all scripts.


Security:
    API for user account database management.


Additional scripts:
    create_user.py - creates users in FattyDatabase
    setup_rabbit.py - creates queues and exchanges with its bindings for sample usage.
    setup.py - installs utility package


NOTE: Second part(after '.') of Queue name in communication module is also a routing key for a exchange

