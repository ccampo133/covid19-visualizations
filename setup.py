from codecs import open
from os import path

from setuptools import setup

# Get the long description from the README
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='covid19visuals',
    version='0.1.0',
    description='Various visualizations for COVID-19 data.',
    long_description=long_description,
    author='Chris Campo',
    author_email='ccampo.progs@gmail.com',
    install_requires=[
        'requests==2.22.0',
        'pandas==1.0.3',
        'matplotlib==3.2.1',
        'pystache==0.5.4'
    ],
    packages=['covid19visuals'],
    entry_points={
        'console_scripts': ['covid19visuals=covid19visuals.cli:main']
    },
)
