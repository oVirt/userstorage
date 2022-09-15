# Copyright (C) 2019 Nir Soffer
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import division

import glob
import logging
import os
import shutil
import subprocess
import tempfile

from . import backend
from . import errors
from . import osutil

log = logging.getLogger("userstorage")


class Mount(backend.Base):
    """
    A mounted filesystem on top of a loop device.
    """

    def __init__(self, loop, fstype="ext4"):
        self._loop = loop
        self.fstype = fstype
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
            osutil.chown(self.path, os.geteuid(), os.getegid())

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

    def tmpdir(self):
        """
        Create and return a TemporaryDirectory in the current
        mounted filesystem. Can be used as a context manager.
        """
        return tempfile.TemporaryDirectory(dir=self.path)

    # Helpers

    def _create_filesystem(self):
        log.debug("Creating %s file system on %s",
                  self.fstype, self._loop.path)
        try:
            subprocess.check_call(
                ["sudo", "mkfs", "-t", self.fstype, "-q", self._loop.path])
        except subprocess.CalledProcessError as e:
            raise errors.CreateFailed(
                "Error creating filesystem: {}".format(e))

        self._wait_for_udev_events(10)

    def _mount_loop(self):
        try:
            subprocess.check_call([
                "sudo",
                "mount",
                "-t", self.fstype,
                self._loop.path,
                self.path
            ])
        except subprocess.CalledProcessError as e:
            raise errors.CreateFailed(
                "Error mounting loop device: {}".format(e))

    def _unmount_loop(self):
        subprocess.check_call(["sudo", "umount", self.path])

    def _wait_for_udev_events(self, timeout=10):
        log.debug("Waiting up to %s seconds for udev events", timeout)
        subprocess.check_call(
            ["udevadm", "settle", "--timeout={}".format(timeout)])
