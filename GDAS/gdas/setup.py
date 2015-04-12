__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Utility package',
      version='1.0',
      description='Utilitiy package for GDAS system',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/', [
              'create_user',
              'create_exchange'
          ])
      ],
      packages=[
          'util.communication',
          'util.database',
          'util.input',
          'util.security',
      ],
      install_requires=[
          'flask',
          'pika',
          'pymongo'
      ]
)