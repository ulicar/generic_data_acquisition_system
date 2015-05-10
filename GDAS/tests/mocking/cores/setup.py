__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Core',
      version='1.0',
      description='GDAS testing core',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/core', [
              'simpleCore.py',
              'simplePassiveCore.py',
              'simpleActiveCore.py'
          ]),
          ('/etc/gdas/core', [
              'simplePassiveCore.uwsgi.ini.default',
              'simplePassiveCore.nginx.ini.default'
          ])
      ],
      install_requires=[
          'flask==0.10'
      ])