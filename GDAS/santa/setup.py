__author__ = 'jdomsic'

from setuptools import setup

setup(name='GDAS Santa',
      version='1.0',
      description='GDAS Santa database interface',
      author='Josip Domsic',
      author_email='josip.domsic@gmail.com',
      license='MIT',
      url='https://github.com/ulicar/generic_data_acquisition_system',
      data_files=[
          ('/opt/gdas/santa', [
              'santa.py'
          ]),
          ('/etc/gdas/wizard', [
              'santa.ini.default',
              'santa.conf',
              'santa.uwsgi.ini.default',
              'santa.nginx.ini.default',
              'example.post-data.txt'
              'README.txt'
          ])
      ],
      install_requires=[
          'GDAS',
          'flask==0.10.1'
      ])
