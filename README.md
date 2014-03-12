# Introduction

*ImageGridSplitter* is a command-line python utility for splitting big images into a grid of smaller sub-images.


# Requirements

Python 3.x. 

*ImageGridSplitter* also uses the [Pillow] (https://github.com/python-imaging/Pillow) package, but this should be automatically downloaded upon installation.


# Installation

Clone the repo, enter the directory, and type:

```
python setup.py install
```

This will install a command-line utility named `img_grid_split`.


# Usage

Quick usage:

```
img_grid_split input_files [input_files ...]
```

It is possible to specify some extra options, such as the maximum width and/or height for the sub-images. Please, type `img_grid_split -h` for additional help.
