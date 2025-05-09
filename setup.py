# SPDX-FileCopyrightText: oVirt Developers <devel@ovirt.org>
# SPDX-License-Identifier: GPL-2.0-or-later

# flake8: noqa

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="userstorage",
    version="0.6.0",
    author="oVirt Developers",
    author_email="devel@ovirt.org",
    description="Create storage for tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oVirt/userstorage",
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
