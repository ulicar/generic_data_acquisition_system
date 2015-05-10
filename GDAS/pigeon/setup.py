__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Pigdeon',
      version='1.0',
      description='GDAS message selector',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/pigeon', [
              'message_selector.py',
              'message_scheme.py',
              'config.py'
          ]),
          ('/etc/gdas/pigeon', [
              'message_selector.ini.default'
          ])
      ],
      install_requires=[
          'GDAS',
          'validictory'
      ])
