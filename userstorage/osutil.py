# Copyright (C) 2019 Nir Soffer
# SPDX-License-Identifier: GPL-2.0-or-later

import errno
import grp
import logging
import os
import pwd
import subprocess

log = logging.getLogger("userstorage")


def chown(path, uid, gid):
    user = pwd.getpwuid(uid).pw_name
    group = grp.getgrgid(gid).gr_name
    user_group = "{}:{}".format(user, group)
    log.debug("Changing %s ownership to %s", path, user_group)
    subprocess.check_call(["sudo", "chown", "-R", user_group, path])


def create_dir(path):
    log.debug("Creating directory %s", path)
    try:
        os.makedirs(path)
    except EnvironmentError as e:
        if e.errno != errno.EEXIST:
            raise


def remove_file(path):
    log.debug("Removing file %s", path)
    try:
        os.remove(path)
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise


def remove_dir(path):
    log.debug("Removing directory %s", path)
    try:
        os.rmdir(path)
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
