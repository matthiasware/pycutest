from setuptools import setup
from setuptools import find_packages


setup(name="pycutest",
      packages=find_packages(),
      version="0.5",
      description="An interface for the CUTEST package",
      url="https://github.com/matthiasware/pycutest.git",
      package_data={'': ['*.pyx', '*.pxd']},
      test_suite='nose.collector',
      tests_require=['nose']
      )
