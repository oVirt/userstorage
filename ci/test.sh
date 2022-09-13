#!/bin/bash -e

create_loop_devices() {
    local last=$(($1-1))
    local min
    for min in `seq 0 $last`; do
        local name=/dev/loop$min
        if [ ! -e "$name" ]; then
            echo "Creating loop device $name"
            mknod --mode 0666 $name b 7 $min
        fi
    done
}

teardown_storage() {
    python3 -m userstorage delete example_config.py \
        || echo "WARNING: Ingoring error while tearing down user storage"
}

create_loop_devices 16

# Install userstorage.
python3 -m pip install .
# Setup storage.
python3 -m userstorage create example_config.py
# Teardown storage before exit.
trap teardown_storage EXIT
# Run tests (skip provision tests in the CI, since loop device creating is flaky)
tox -e py36 -- -m "not sudo"