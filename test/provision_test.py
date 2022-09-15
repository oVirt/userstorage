# Copyright (C) 2019 Nir Soffer
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import division

import os
import subprocess
import sys

import pytest

import userstorage

CONFIG = "test/provision_config.py"


class FakeMissingError(Exception):
    """
    Fake Exception to monkeypatch userstorage.missing_handler.
    """


def run(command):
    subprocess.check_call([
        sys.executable,
        "-m", "userstorage",
        command,
        CONFIG
    ])


@pytest.fixture(scope='module')
def config():
    backends = userstorage.load_config(CONFIG).BACKENDS
    yield backends


@pytest.fixture
def cleanup():
    yield
    run("delete")


@pytest.mark.sudo
def test_provision(config, cleanup):
    run("create")

    for b in config.values():
        assert b.exists()

        st = os.stat(b.path)
        assert st.st_uid == os.geteuid()
        assert st.st_gid == os.getegid()

    devices = [os.path.realpath(b.path) for b in config.values()
               if isinstance(b, userstorage.LoopDevice)]

    run("delete")

    for b in config.values():
        assert not b.exists()

    for dev in devices:
        st = os.stat(dev)
        assert st.st_uid == 0
        assert st.st_gid == 6  # disk


@pytest.mark.sudo
def test_create_twice(config, cleanup):
    run("create")
    run("create")

    for b in config.values():
        assert b.exists()


@pytest.mark.sudo
def test_delete_twice(config, cleanup):
    for b in config.values():
        assert not b.exists()

    run("delete")

    for b in config.values():
        assert not b.exists()


@pytest.mark.sudo
def test_storage_not_available(config, monkeypatch, cleanup):
    def _handler(msg):
        raise FakeMissingError(msg)
    monkeypatch.setattr(userstorage, "missing_handler", _handler)

    for storage in config.values():
        # Setup a storage without create raises FakeMissingError
        with pytest.raises(FakeMissingError):
            with storage:
                pass
