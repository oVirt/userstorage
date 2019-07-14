# Copyright (C) 2019 Nir Soffer
# This program is free software; see LICENSE for more info.

from __future__ import absolute_import
from __future__ import division

import argparse
import logging

from . import backend
from . import config
from . import osutil

log = logging.getLogger("userstorage")


def main():
    parser = argparse.ArgumentParser(
        description='Set up storage tests')
    parser.add_argument("command", choices=["create", "delete"])
    parser.add_argument("config_file", help="Configuration file")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(name)s] %(levelname)-7s %(message)s")

    cfg = config.load_config(args.config_file)

    if args.command == "create":
        create(cfg)
    elif args.command == "delete":
        delete(cfg)


def create(cfg):
    osutil.create_dir(cfg.BASE_DIR)

    for b in cfg.BACKENDS.values():
        try:
            b.create()
        except backend.Error as e:
            if b.required:
                raise
            log.warning("Skipping %s storage: %s", b.name, e)


def delete(cfg):
    for b in cfg.BACKENDS.values():
        b.delete()

    osutil.remove_dir(cfg.BASE_DIR)


if __name__ == "__main__":
    main()
