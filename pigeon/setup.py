__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Pigdeon',
      version='1.0',
      description='GDAS Pigeon message selector',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/pigeon', [
              'pigeon.py',
              'message_scheme.py',
              'config.py'
          ]),
          ('/etc/gdas/pigeon', [
              'pigeon.ini.default.hgk',
              'pigeon.ini.default.unizg-1',
              'pigeon.ini.default.unizg-2',
              'pigeon.ini.default.usa',
              'README.txt'
          ])
      ],
      install_requires=[
          'GDAS',
          'validictory'
      ])
