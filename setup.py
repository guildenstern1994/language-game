

#!/usr/bin/env python

from setuptools import setup, find_packages


reqs = [
	"numpy"
]

setup(name='LanguageGame',
      version='0.1',
      description='Game',
      install_requires=[reqs],
      author='Jonathan Engel',
      author_email='jengel2@protonmail.com',
      packages=find_packages(),
     )


