Wizard is responsible for accepting all data packages.

First, username and password of uploader is checked against existing user in database.
Second, data is pushed to message queue.

To test uWSGI: (reads data from /etc/gdas/wizard/)
 (1) check the HTTP/SOCKET in wizard.uwsgi.ini.default
 (2) sudo uwsgi --ini wizard.uwsgi.ini.default
 (3) in browser http://localhost:[PORT]/api/wizard/upload
 * you should get METHOD not allowed


To test Nginx:
 (1) make sure it has application information in site-enabled and site-available
 (2) Uwsgi configuration has SOCKET
 .. same as testing UWSGI
