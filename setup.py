__author__ = 'ngdelamo'

from setuptools import setup, find_packages

setup(
    name='ImageGridSplitter',
    version='0.0.2',
    author='Nacho Garcia',
    packages=find_packages(exclude=['tests/', 'tests.*']),
    install_requires=['Pillow>=2.3.0'],
    entry_points={
        'console_scripts': ['img_grid_split = ImageGridSplitter:main']
    },
    test_suite='nose.collector',
    zip_safe=True,
)
