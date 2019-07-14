# Copyright (C) 2019 Nir Soffer
# This program is free software; see LICENSE for more info.

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

import imp
import os


def load_config(filename):
    """
    Load user configuration module.
    """
    basepath = os.path.splitext(filename)[0]
    module_dir, module_name = os.path.split(basepath)
    fp, pathname, description = imp.find_module(module_name, [module_dir])
    try:
        return imp.load_module(module_name, fp, pathname, description)
    finally:
        if fp:
            fp.close()
