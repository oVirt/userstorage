# Copyright (C) 2019 Nir Soffer
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import division

import os
import subprocess
import sys

import pytest
from _pytest.outcomes import XFailed

import userstorage

CONFIG = "test/provision_config.py"
BACKENDS = userstorage.load_config(CONFIG).BACKENDS


def run(command):
    subprocess.check_call([
        sys.executable,
        "-m", "userstorage",
        command,
        CONFIG
    ])


@pytest.fixture
def cleanup():
    yield
    run("delete")


@pytest.mark.sudo
def test_provision(cleanup):
    run("create")

    for b in BACKENDS.values():
        assert b.exists()

        st = os.stat(b.path)
        assert st.st_uid == os.geteuid()
        assert st.st_gid == os.getegid()

    devices = [os.path.realpath(b.path) for b in BACKENDS.values()
               if isinstance(b, userstorage.LoopDevice)]

    run("delete")

    for b in BACKENDS.values():
        assert not b.exists()

    for dev in devices:
        st = os.stat(dev)
        assert st.st_uid == 0
        assert st.st_gid == 6  # disk


@pytest.mark.sudo
def test_create_twice(cleanup):
    run("create")
    run("create")

    for b in BACKENDS.values():
        assert b.exists()


@pytest.mark.sudo
def test_delete_twice(cleanup):
    for b in BACKENDS.values():
        assert not b.exists()

    run("delete")

    for b in BACKENDS.values():
        assert not b.exists()


@pytest.mark.sudo
def test_storage_not_available(cleanup):
    for storage in BACKENDS.values():
        # Setup a storage without create is xfailed
        with pytest.raises(XFailed):
            with storage:
                pass
