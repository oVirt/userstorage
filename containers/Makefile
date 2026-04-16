# Copyright (C) 2022 Albert Esteve
# SPDX-License-Identifier: GPL-2.0-or-later

targets := centos-9 centos-10 almalinux-9 almalinux-10
prefix := userstorage-test

.PHONY: $(targets) push

all: $(targets)

$(targets):
	podman build -t $(prefix):$@ -f $@.containerfile .

push:
	for name in $(targets); do \
		podman push $(prefix):$$name quay.io/ovirt/$(prefix):$$name; \
	done