"""
Configuration for provisioning test.
"""

from userstorage import LoopDevice, Mount, File

MiB = 1024**2

BASE_DIR = "/var/tmp/provision-test"

BACKENDS = {

    "block-512": LoopDevice(
        base_dir=BASE_DIR,
        name="block-512",
        size=10 * MiB,
        sector_size=512,
    ),

    "block-4k": LoopDevice(
        base_dir=BASE_DIR,
        name="block-4k",
        size=10 * MiB,
        sector_size=4096,
    ),

    "mount-512": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-512",
            size=10 * MiB,
            sector_size=512,
        )
    ),

    "mount-4k": Mount(
        LoopDevice(
            base_dir=BASE_DIR,
            name="mount-4k",
            size=10 * MiB,
            sector_size=4096,
        )
    ),

    "file-512": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-512",
                size=10 * MiB,
                sector_size=512,
            )
        )
    ),

    "file-4k": File(
        Mount(
            LoopDevice(
                base_dir=BASE_DIR,
                name="file-4k",
                size=10 * MiB,
                sector_size=4096,
            )
        )
    ),
}
