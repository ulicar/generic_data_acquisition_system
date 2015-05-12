__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS test cores',
      version='1.0',
      description='GDAS testing cores for Wizard',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/test/cores', [
              '__init__.py',
              'coreCreator.py',
              'simpleCore.py',
              'simpleActiveCore.py',
              'simplePassiveCore.py',
          ]),
          ('/opt/gdas/test/cores/sensorNodes', [
              'sensorNodes/__init__.py',
              'counterNode.py',
              'sensorNodes/cpuNode.py',
              'sensorNodes/doorNode.py',
              'sensorNodes/humidityNode.py',
              'sensorNodes/lightNode.py',
              'sensorNodes/sensorNode.py',
              'sensorNodes/temperatureNode.py'
          ]),
          ('/etc/gdas/test/cores', [
              'simpleActiveCore.ini.default',
              'simplePassiveCore.ini.default',
              'simplePassiveCore.uwsgi.ini.default',
              'simplePassiveCore.nginx.ini.default'
          ])
      ],
      install_requires=[
          'flask==0.10.1'
      ])
