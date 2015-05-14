__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Hobbit',
      version='1.0',
      description='GDAS Hobbit message requester',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/hobbit', [
              'hobbit.py',
              'config.py'
          ]),
          ('/etc/gdas/hobbit', [
              'hobbit.ini.default.fer',
              'hobbit.ini.default.fsb',
              'hobbit.ini.default.tvz',
              'hobbit.ini.default.mit',
              'hobbit.ini.default.ucla',
              'README.txt'

          ])
      ],
      install_requires=[
          'requests',
          'validictory',
          'GDAS'
      ]
)