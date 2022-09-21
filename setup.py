# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# flake8: noqa

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="userstorage",
    version="0.6.0",
    author="Nir Soffer",
    author_email="nirsof@gmail.com",
    description="Create storage for tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nirs/userstorage",
    packages=["userstorage"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
    ],
    entry_points = {
        'console_scripts': ['userstorage=userstorage.__main__:main'],
    }
)
