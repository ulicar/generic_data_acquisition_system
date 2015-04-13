__author__ = 'jdomsic'

from distutils.core import setup

setup(name='GDAS Hobbit',
      version='1.0',
      description='GDAS message requester',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/hobbit', [
              'message_requester.py',
              'config.py'
          ]),
          ('/etc/gdas/hobbit', [
              'message_requester.ini.default'
          ])
      ]
)