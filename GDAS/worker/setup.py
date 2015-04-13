__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Worker',
      version='1.0',
      description='GDAS message processor',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/worker', [
              'message_processor.py',
              'config.py'
          ]),
          ('/etc/gdas/worker', [
              'message_processor.ini.default'
          ])
      ],
      install_requires=[
         'GDAS.utils',
         'validictory',
         'flask=0.10'
      ]
)