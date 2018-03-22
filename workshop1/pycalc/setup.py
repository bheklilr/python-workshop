from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name="pycalc",
    version=version,
    author="Aaron Stevens",
    author_email="bheklilr2@gmail.com",
    description="A simple calculator app",
    packages=find_packages('.', exclude=['docs', 'tests']),
)
