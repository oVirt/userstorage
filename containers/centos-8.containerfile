# SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

FROM quay.io/centos/centos:stream8

# Runtime packages.
RUN dnf update -y \
    && dnf install -y \
        e2fsprogs \
        sudo \
        systemd-udev \
        util-linux \
        xfsprogs \
        python3-devel \
        python3-pip \
    && dnf clean all

# Developemnt tools.
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --requirement requirements.txt