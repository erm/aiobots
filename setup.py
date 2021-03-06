import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aiobots',
    version='0.0.1',
    packages=['aiobots'],
    install_requires=[
        'aiohttp',
        'aiohttp-jinja2',
    ],
    license='MIT License',
    author='Jordan E.',
    author_email='jermff@gmail.com',
)
