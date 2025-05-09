# Copyright (C) oVirt Developers <devel@ovirt.org>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Storage configuration loader.

The configuration file is loaded by userstorage tool providing the storage and
by test module consuming the storage.

The configuration file is a python module, providing these names:

    # Directory keeping storage files.
    BASE_DIR = "/var/tmp/my-project-storage"

    # Dictionary of backends.
    BACKENDS = {}

See exampleconf.py example for more info.
"""

import importlib.util
import os


def load_config(filename):
    """
    Load user configuration module.
    """
    basepath = os.path.splitext(filename)[0]
    _, module_name = os.path.split(basepath)
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
