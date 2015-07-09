Santa is responsible for reading database / database api.

  APIs:

      /api/santa/fetch {POST}

      Post data:
      {
      'gdas': {
            'user' : USERNAME,
            'cores': [CORE, CORE],
            'modules': [MODULE, MOUDLE, ...],
            'time': {
                'from': %YYYY-%MM-%DDT%hh:%mm:%ss,
                'to': %YYYY-%MM-%DDT%hh:%mm:%ss}
            }

      }

      Required: (USER or CORES) and TIME
      Optional: MODULES (wildcard is '*')


To test uWSGI: (reads data from /etc/gdas/santa/)
 (1) check the HTTP/SOCKET in santa.uwsgi.ini.default
 (2) sudo uwsgi --ini santa.uwsgi.ini.default
 (3) in browser http://localhost:[PORT]/api/santa/fetch
 * you should get METHOD not allowed (if using GET)


To test Nginx:
 (1) make sure it has application information in site-enabled and site-available
 (2) Uwsgi configuration has SOCKET
 .. same as testing UWSGI
