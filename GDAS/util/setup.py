__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS',
      version='1.0',
      description='Utility package for GDAS system',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/', [
              'create_user.py',
              'setup_rabbit.py'
          ]),
          ('/etc/gdas/README.txt')
      ],
      packages=[
          'GDAS',
          'GDAS.utils',
          'GDAS.utils.communication',
          'GDAS.utils.database',
          'GDAS.utils.input',
          'GDAS.utils.security'
      ],
      install_requires=[
          'flask==0.10.1',
          'pika==0.9.14',
          'pymongo==3.0',
          'validictory'
      ])
