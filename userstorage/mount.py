# Copyright (C) 2019 Nir Soffer
# This program is free software; see LICENSE for more info.

from __future__ import absolute_import
from __future__ import division

import glob
import logging
import os
import shutil
import subprocess

from . import backend
from . import osutil

log = logging.getLogger("userstorage")


class Mount(backend.Base):
    """
    A mounted filesystem on top of a loop device.
    """

    def __init__(self, loop):
        self._loop = loop
        self.path = os.path.join(loop.base_dir, loop.name + "-mount")

    # Backend interface

    @property
    def name(self):
        return self._loop.name

    @property
    def sector_size(self):
        return self._loop.sector_size

    @property
    def required(self):
        return self._loop.required

    def create(self):
        if self.exists():
            log.debug("Reusing mount %s", self.path)
            return

        self._loop.create()

        log.info("Creating filesystem %s", self.path)
        self._create_filesystem()
        osutil.create_dir(self.path)
        self._mount_loop()

        if os.geteuid() != 0:
            osutil.chown(self.path)

    def delete(self):
        log.info("Unmounting filesystem %s", self.path)

        if self.exists():
            self._unmount_loop()

        osutil.remove_dir(self.path)

        self._loop.delete()

    def exists(self):
        with open("/proc/self/mounts") as f:
            for line in f:
                if self.path in line:
                    return True
        return False

    def setup(self):
        pattern = os.path.join(self.path, "*")
        for path in glob.iglob(pattern):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    # Helpers

    def _create_filesystem(self):
        # TODO: Use -t xfs (requires xfsprogs package).
        subprocess.check_call(["sudo", "mkfs", "-q", self._loop.path])

    def _mount_loop(self):
        subprocess.check_call(["sudo", "mount", self._loop.path, self.path])

    def _unmount_loop(self):
        subprocess.check_call(["sudo", "umount", self.path])
