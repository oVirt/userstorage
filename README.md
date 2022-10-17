<!--
SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
SPDX-License-Identifier: GPL-2.0-or-later
-->

# userstorage

[![Package version](https://img.shields.io/pypi/v/userstorage)](https://pypi.org/project/userstorage/)
[![Python versions](https://img.shields.io/pypi/pyversions/userstorage)](https://pypi.org/project/userstorage/)
[![Downloads per month](https://img.shields.io/pypi/dm/userstorage)](https://pypi.org/project/userstorage/)
[![CI status](https://github.com/nirs/userstorage/actions/workflows/ci.yml/badge.svg)](https://github.com/nirs/userstorage/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/nirs/userstorage)](https://pypi.org/project/userstorage/)

Helper for setting up storage for tests.


## Overview

Some tests need more than a temporary directory on the local file
system. One example is testing block device with 4k sector size, or
testing a filesystem on top of such a block device.

You can create storage using loop devices and mounts in test fixtures,
but creating devices and mounts requires root. Do you really want to run
all your tests as root, when the code under test should not run as root?

The userstorage tool solves this problem by creating storage for tests
before running the tests, and making the storage available to the
current user. Once you created the storage, you can run the tests
quickly as yourself directly from your editor.

## Requirements

On Fedora / CentOS you need to install these packages:

    dnf install \
        e2fsprogs \
        sudo \
        systemd-udev \
        util-linux \
        xfsprogs

Some packages are typically installed on your machine, but you may need
to add them to CI environment or container.


## Installing

Use pip:

    python3 -m pip install --user userstorage


## Creating configuration file

The userstorage tool creates storage based on configuration file that
you must provide.

The configuration module is used both by the userstorage tool to
provision the storage, and by the tests consuming the storage.

The configuration module typically starts by importing the required
backends:

    from userstorage import File

The configuration module must define these names:

    # Where storage is provisioned.
    BASE_DIR = "/path/to/my/storage"

    # Storage configurations needed by the tests.
    BACKENDS = {}

See [example_config.py](https://raw.githubusercontent.com/nirs/userstorage/master/example_config.py)
for example configuration used by the tests for this project.


## Creating storage

To create the storage described in example_config.py, run:

    userstorage create example_config.py

This can be run once when creating a development environment, and must
be run again after rebooting the host.

If you want to delete the storage, run:

    userstorage delete example_config.py

There is no need to delete the storage normally. The loop devices are
backed up by sparse files and do not consume much resources.


## Consuming the storage in your tests

See test/consume_test.py for example test module consuming storage
set up by userstorage tool, and the example_config.py module.

Note that some storage may not be available on some systems. If a storage is
not available, it will raise `userstorage.Missing`.
The behaviour for missing storage can be overriden from your tests
(e.g., to mark the test as xfail if needed) by doing:

    userstorage.missing_handler = pytest.xfail


## Ensuring test isolation

Reusing the same storage for all tests introduce the problem of old test
data breaking other tests, or causing test to pass when they should
fail.

To avoid this issues, you should call backend's setup() methods before
using the storage in a test, and teardown() after running the tests.
This ensures that old data from other tests will not be seen by this
test.


## How it works?

The userstorage tool creates this directory layout in the BASE_DIR
defined in the configuration module:

    $ tree /var/tmp/example-storage/
    /var/tmp/example-storage/
    ├── block-4k-backing
    ├── block-4k-loop -> /dev/loop2
    ├── block-512-backing
    ├── block-512-loop -> /dev/loop3
    ├── file-4k-backing
    ├── file-4k-loop -> /dev/loop4
    ├── file-4k-mount
    │   ├── file
    │   └── lost+found [error opening dir]
    ├── file-512-backing
    ├── file-512-loop -> /dev/loop5
    └── file-512-mount
        ├── file
        └── lost+found [error opening dir]

The symbolic links (e.g. file-4k-loop) link to the loop devices created
by the tool (/dev/loop4), and used to delete the storage later.

The actual file used for the tests are created inside the mounted
filesystem (/var/tmp/example-storage/file-4k-mount/file).


## Projects using userstorage

- [ovirt-imageio](https://github.com/oVirt/ovirt-imageio)
- [vdsm](https://github.com/oVirt/vdsm)
- [sanlock](https://pagure.io/sanlock) - embeds a very early version

(Please add your project here)


## Contributing

If you found a bug, please open an issue.

If you have an idea for improving this tool, please open an issue to
discuss the idea.

For trivial changes please send a pull request.


## Running the tests

To run the tests you need to install tox. You can use tox from your
distribution (e.g., python3-tox on Fedora), or install it using
pip.

Before running the tests, create the example storage:

    python3 -m userstorage create example_config.py

To run the tests:

    tox

If you want to change storage layout, best delete the example storage:

    python3 -m userstorage delete example_config.py
