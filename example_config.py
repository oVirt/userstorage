# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Example userstorage configuration module.
"""

import userstorage
from userstorage import LoopDevice, Mount, File

import pytest


# Mark tests as xfail when the storage they need is missing.
userstorage.missing_handler = pytest.xfail

GiB = 1024**3

# Base directory for provisioned storage.
#
# This is the directory where backing files, symlinks to loop devices, and
# mount directories are created.

BASE_DIR = "/var/tmp/example-storage"


# Dictionary of backends.
#
# Here is an example configuration providing all builtin backend types. Note
# that 4k storage is defined as optional since creating loop device with 4k
# storgae is not supported on all environments and may be flaky in some
# supported environments.

BACKENDS = {

    "block-512": LoopDevice(
        base_dir=BASE_DIR,
        name="block-512",
        size=GiB,
        sector_size=512,
    ),

    "block-4k": LoopDevice(
        base_dir=BASE_DIR,
        name="block-4k",
        size=GiB,
        sector_size=4096,
        required=False,
    ),

    "mount-512-ext2": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512-ext2",
            size=GiB,
            sector_size=512,
        ),
        fstype="ext2",
    ),

    "mount-512-ext4": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512-ext4",
            size=GiB,
            sector_size=512,
        ),
        fstype="ext4",
    ),

    "mount-512-xfs": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512-xfs",
            size=GiB,
            sector_size=512,
        ),
        fstype="xfs",
    ),

    "mount-4k-ext2": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k-ext2",
            size=GiB,
            sector_size=4096,
            required=False,
        ),
        fstype="ext2",
    ),

    "mount-4k-ext4": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k-ext4",
            size=GiB,
            sector_size=4096,
            required=False,
        ),
        fstype="ext4",
    ),

    "mount-4k-xfs": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k-xfs",
            size=GiB,
            sector_size=4096,
            required=False,
        ),
        fstype="xfs",
    ),

    "file-512": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-512",
                size=GiB,
                sector_size=512,
            )
        )
    ),

    "file-4k": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-4k",
                size=GiB,
                sector_size=4096,
                required=False,
            )
        )
    ),
}
