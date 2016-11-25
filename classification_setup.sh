#!/bin/bash
# Create a directory
mkdir article_classification
cd article_classification

# install  homebrew

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
export PATH=/usr/local/bin:$PATH
# install Python
brew install Python

# Set Python to global path and set up the default config
export PATH=/usr/local/share/python:$PATH

pip install virtualenv
pip install virtualenvwrapper
pip install numpy
brew install gfortran
pip install scipy
brew install freetype
pip install matplotlib
pip install ipython[all]

# set up the useful config
pip install grocery 
pip install nytimesarticle
