# Copyright (C) 2019 Nir Soffer
# SPDX-License-Identifier: GPL-2.0-or-later

# flake8: noqa

# Backends.
from userstorage.loop import LoopDevice
from userstorage.mount import Mount
from userstorage.file import File

# Helpers.
from userstorage.config import load_config

# Errors.
from userstorage.errors import (
    Error,
    Unsupported,
    CreateFailed,
    Missing,
)


def missing_handler(msg):
    """
    Should be called when entering the context without having created
    the associated storage.

    Clients can override if needed.
    """
    raise Missing(msg)
