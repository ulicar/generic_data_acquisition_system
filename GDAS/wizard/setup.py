__author__ = 'jdomsic'

from distutils.core import setup

setup(name='GDAS Wizard',
      version='1.0',
      description='GDAS message collector',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      url='https://github.com/ulicar/generic_data_acquisition_system',

      data_files=[
          ('/opt/gdas/wizard', [
              'message_collector.py',
              'config.py'
          ]),
          ('/etc/gdas/wizard', [
              'message_collector.ini.default'
          ])
      ]
)