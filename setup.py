from setuptools import setup
from setuptools import find_packages


setup(name="pycutest",
      packages=find_packages(),
      version="0.5",
      author_email="matthias.mitterreiter@uni-jena.de",
      description="An interface for the CUTEST package",
      url="https://bitbucket.org/matthiasware/pycutest",
      package_data={'': ['*.pyx', '*.pxd']},
      test_suite='nose.collector',
      tests_require=['nose']
      )
