"""
Example userstorage configuration module.
"""

from userstorage import LoopDevice, Mount, File

GiB = 1024**3

# Base directory for provisioned storage.
#
# This is the directory where backing files, symlinks to loop devices, and
# mount directories are created.

BASE_DIR = "/var/tmp/example-storage"


# Dictionary of backends.
#
# Here is an example configuration providing all builtin backend types. Note
# that 4k storage is defined as optional since creating loop device with 4k
# storgae is not supported on all environments and may be flaky in some
# supported environments.

BACKENDS = {

    "block-512": LoopDevice(
        base_dir=BASE_DIR,
        name="block-512",
        size=GiB,
        sector_size=512,
    ),

    "block-4k": LoopDevice(
        base_dir=BASE_DIR,
        name="block-4k",
        size=GiB,
        sector_size=4096,
        required=False,
    ),

    "mount-512": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512",
            size=GiB,
            sector_size=512,
        )
    ),

    "mount-4k": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k",
            size=GiB,
            sector_size=4096,
            required=False,
        )
    ),

    "file-512": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-512",
                size=GiB,
                sector_size=512,
            )
        )
    ),

    "file-4k": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-4k",
                size=GiB,
                sector_size=4096,
                required=False,
            )
        )
    ),
}
