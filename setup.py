__author__ = 'ngdelamo'

from setuptools import setup, find_packages

setup(
    name='ImageGridSplitter',
    version='0.0.1',
    author='Nacho Garcia',
    packages=find_packages(exclude=['tests/', 'tests.*']),
    entry_points={
        'console_scripts': ['img_grid_split = ImageGridSplitter:img_grid_split']
    },
    test_suite='nose.collector', zip_safe=True
)
