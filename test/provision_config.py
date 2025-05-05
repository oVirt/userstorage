# SPDX-FileCopyrightText: oVirt Developers <devel@ovirt.org>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Configuration for provisioning test.
"""

import userstorage
from userstorage import LoopDevice, Mount, File

import pytest


userstorage.missing_handler = pytest.xfail

# mkfs.xfs requires at leat 4096 blocks (16 MiB). Lets double that value to
# keep a way from the limits.
SIZE = 32 * 1024**2

BASE_DIR = "/var/tmp/provision-test"

BACKENDS = {

    "block-512": LoopDevice(
        base_dir=BASE_DIR,
        name="block-512",
        size=SIZE,
        sector_size=512,
    ),

    "block-4k": LoopDevice(
        base_dir=BASE_DIR,
        name="block-4k",
        size=SIZE,
        sector_size=4096,
    ),

    "mount-512": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512",
            size=SIZE,
            sector_size=512,
        ),
        fstype="ext4",
    ),

    "mount-4k": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k",
            size=SIZE,
            sector_size=4096,
        ),
        fstype="xfs",
    ),

    "file-512": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-512",
                size=SIZE,
                sector_size=512,
            )
        )
    ),

    "file-4k": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-4k",
                size=SIZE,
                sector_size=4096,
            )
        )
    ),
}
