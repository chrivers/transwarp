#!/usr/bin/env python3
import os
from setuptools import setup

setup(
    name = "transwarp",
    version = "0.1.0",
    author = "Christian Iversen",
    author_email = "ci@iversenit.dk",
    description = """The transwarp compiler parses Simple Type Format (.stf) input file,
    and renders templates, using this data structure. This allows the
    user to build documentation, test, protocol implementation and
    everything else, from one common source""",
    license = "GPLv3",
    url = "https://github.com/chrivers/transwarp",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Other Scripting Engines",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
)
