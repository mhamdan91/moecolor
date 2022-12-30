import os
from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = 'Python libary to quickly label data/images.'
LONG_DESCRIPTION = open('README.md').read()
setup(
    name="moecolor",
    version=VERSION,
    author="mhamdan91 (Hamdan, Muhammad)",
    author_email="<mhamdan-91@hotmail.com>",
    url='https://github.com/mhamdan91/moecolor',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'gui', 'labeling', 'machine-learning', 'labeler', 'classification', 'images', 'annotation'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
)