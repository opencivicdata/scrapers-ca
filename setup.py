# @see http://pythonhosted.org/an_example_pypi_project/setuptools.html
# @see http://pythonhosted.org/setuptools/setuptools.html
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='scrapers_ca',
    version='0.0.1',
    author='Open North',
    author_email='info@opennorth.ca',
    description='Canadian legislative scrapers',
    license='MIT',
    url='https://github.com/opencivicdata/scrapers-ca',
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'lxml',
    ]
)
