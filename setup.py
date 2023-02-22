import os
from setuptools import setup, find_packages
from moecolor.version import __version__
VERSION = __version__
DESCRIPTION = 'Python Libary to print colored and styled text in terminal. ' \
              'Offers color-specific configuration by providing 24bit hex '  \
              'or RGB values as well 256-color mode.'
LONG_DESCRIPTION = open('README.md').read()
setup(
    name="moecolor",
    version=VERSION,
    author="mhamdan91 (Hamdan, Muhammad)",
    author_email="<mhamdan.dev@gmail.com>",
    url='https://github.com/mhamdan91/moecolor',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'color', 'terminal', 'text', 'styling', 'ansi',
              'coloring text', 'text styling', 'text formatting', 'formatting'],
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