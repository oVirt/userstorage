# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later


class Error(Exception):
    """
    Base class for backend errors.
    """


class Unsupported(Error):
    """
    May be raised in create() if backend is not supported on the current
    system.
    """


class CreateFailed(Error):
    """
    May be raised in create() if backend is supported but creating backend has
    failed.
    """


class Missing(Error):
    """
    May be raised in __enter__() if backend is not created before setup().
    """
