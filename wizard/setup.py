__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Wizard',
      version='1.0',
      description='GDAS Wizard message collector',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/wizard', [
              'wizard.py'
          ]),
          ('/etc/gdas/wizard', [
              'wizard.ini.default',
              'wizard.conf',
              'wizard.uwsgi.ini.default',
              'wizard.nginx.ini.default',
              'README.txt'
          ])
      ],
      install_requires=[
          'GDAS',
          'flask==0.10.1'
      ])
