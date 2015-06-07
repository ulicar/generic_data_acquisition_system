__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS apprentice',
      version='1.0',
      description='GDAS apprentice message requester',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/apprentice', [
              'apprentice.py',
              'config.py'
          ]),
          ('/etc/gdas/apprentice', [
              'apprentice.ini.default.fer',
              'apprentice.ini.default.fsb',
              'apprentice.ini.default.tvz',
              'apprentice.ini.default.mit',
              'apprentice.ini.default.ucla',
              'README.txt'

          ])
      ],
      install_requires=[
          'requests',
          'validictory',
          'GDAS'
      ]
)