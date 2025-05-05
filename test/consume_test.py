# Copyright (C) oVirt Developers <devel@ovirt.org>
# SPDX-License-Identifier: GPL-2.0-or-later

import errno
import io
import mmap
import os
import stat
import logging

from pathlib import Path
from contextlib import closing

import pytest

import userstorage

BACKENDS = userstorage.load_config("example_config.py").BACKENDS

log = logging.getLogger(__name__)


@pytest.fixture(
    params=[
        BACKENDS["block-512"],
        BACKENDS["block-4k"],
    ],
    ids=str,
)
def user_loop(request):
    with request.param:
        yield request.param


@pytest.fixture(
    params=[
        BACKENDS["mount-512-ext2"],
        BACKENDS["mount-512-ext4"],
        BACKENDS["mount-512-xfs"],
        BACKENDS["mount-4k-ext2"],
        BACKENDS["mount-4k-ext4"],
        BACKENDS["mount-4k-xfs"],
    ],
    ids=str,
)
def user_mount(request):
    with request.param:
        yield request.param


@pytest.fixture(
    params=[
        BACKENDS["file-512"],
        BACKENDS["file-4k"],
    ],
    ids=str,
)
def user_file(request):
    with request.param:
        yield request.param


def test_loop_device(user_loop):
    assert is_block_device(user_loop.path)
    assert logical_block_size(user_loop.path) == user_loop.sector_size


def test_mount(user_mount):
    assert os.path.isdir(user_mount.path)

    filename = os.path.join(user_mount.path, "file")
    with open(filename, "w") as f:
        f.truncate(4096)

    if user_mount.fstype == "ext2":
        log.warning("block size detection broken since kernel 5.5")
    else:
        assert detect_block_size(filename) == user_mount.sector_size


def test_mount_tmpdir(user_mount):
    with user_mount.tmpdir() as tmpdir:
        assert os.path.isdir(tmpdir)
        # Check that tmpdir is relative to the mount path
        assert Path(user_mount.path) in Path(tmpdir).parents

    assert not os.path.exists(tmpdir)


def test_file(user_file):
    assert os.path.isfile(user_file.path)
    assert detect_block_size(user_file.path) == user_file.sector_size


def is_block_device(path):
    mode = os.stat(path).st_mode
    return stat.S_ISBLK(mode)


def logical_block_size(path):
    realpath = os.path.realpath(path)
    dev = os.path.split(realpath)[1]
    lbs = "/sys/block/{}/queue/logical_block_size".format(dev)
    with open(lbs) as f:
        return int(f.readline())


def detect_block_size(path):
    """
    Detect the minimal block size for direct I/O. This is typically the sector
    size of the underlying storage.
    """
    fd = os.open(path, os.O_RDWR | os.O_DIRECT)
    with io.FileIO(fd, "r+") as f:
        for block_size in (512, 4096):
            buf = mmap.mmap(-1, block_size)
            with closing(buf):
                try:
                    f.write(buf)
                except EnvironmentError as e:
                    if e.errno != errno.EINVAL:
                        raise
                else:
                    return block_size
        raise RuntimeError("Cannot detect block size")
