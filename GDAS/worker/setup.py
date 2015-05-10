__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Worker',
      version='1.0',
      description='GDAS Worker',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/worker', [
              'worker.py',
              'config.py'
          ]),
          ('/etc/gdas/worker', [
              'worker.ini.default'
          ])
      ],
      install_requires=[
          'GDAS',
          'validictory',
          'flask==0.10'
      ])
