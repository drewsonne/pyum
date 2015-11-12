from setuptools import setup, find_packages

setup(
    name='pyum',
    version='0.1',
    description='A library for reading yum repositories and rpm metadata',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[],
    author_email='drew.sonne@gmail.com',
    author='Drew J. Sonne',
    url='https://github.com/drewsonne/pyum'
)
