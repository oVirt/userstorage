# Copyright (C) 2019 Nir Soffer
# This program is free software; see LICENSE for more info.

from __future__ import absolute_import
from __future__ import division


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


class Base(object):
    """
    Base class for backend objects.
    """

    # Name used by the tests to locate this backend. Storage backends must be
    # configured with a unique name.
    name = None

    # Storage logical block size.
    sector_size = 512

    # Path to backend. This can be a regular file, a directory, a block device,
    # or a symlink, depending on the backend.
    path = None

    # Set to False to ignore setup errors. Tests using this storage will handle
    # the missing storage.
    required = True

    # Provisioning storage.

    def create(self):
        """
        Create storage backend.
        """
        raise NotImplementedError

    def delete(self):
        """
        Delete storage backend.
        """
        raise NotImplementedError

    def exists(self):
        """
        Return True if backend was created and can be used in a test.
        """
        raise NotImplementedError

    # Ensuring test isolation.

    def setup(self):
        """
        Should be called before each test to ensure old data from previous
        tests does not break this test.

        Should be called in your pytest fixture before yielding the backed to
        the tests. If you use unittest based tests, should be called in
        setUp().

        Subclass should implemnet if needed.
        """

    def teardown(self):
        """
        Should be called after each test if cleanup is needed.

        Should be called in your pytest fixture after yielding the the backed
        to the tests. If you use unittest based tests, should be called in
        tearDown().

        Subclass should implemnet if needed.
        """

    # Displaying.

    def __str__(self):
        return self.name
