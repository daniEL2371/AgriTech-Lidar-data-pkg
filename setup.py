#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
  readme = readme_file.read()

requirements = ['geopandas', 'PDAL==2.4.2', 'pandas>=1.1.0', 'numpy>=1.19.0', 'laspy==2.0.2' ]
test_requirements = ['pytest>=3', ]

setup(
  author="Daniel Zelalem",
  email="danielzelalemheru@gmail.com",
  python_requires='>=3.6',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  description="Python package for fetching lidar elevation data from USG 3DEP",
  install_requires=requirements,
  long_description=readme,
  include_package_data=True,
  keywords='scripts, lidar',
  name='ABTesting',
  packages=find_packages(include=["./"]),
  tests_require=test_requirements,
  url='https://github.com/eandualem/PythonLidar',
  version='0.1.0',
  zip_safe=False,
)
