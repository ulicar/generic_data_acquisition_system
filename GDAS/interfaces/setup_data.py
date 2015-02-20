__author__ = 'jdomsic'

#description: builds protobuf messages for interfaces.contracts.data

from distutils.core import setup
import os

os.system('./compile_protobuf.sh')

setup(name='python-contracts',
      version='1.0',
      description='GDAS interface for data saving',
      packages=[
          'data'
      ]
)