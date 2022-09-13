# Copyright (C) 2022 Albert Esteve
# SPDX-License-Identifier: GPL-2.0-or-later

targets := centos-8
prefix := userstorage-test

.PHONY: $(targets) push

all: $(targets)

$(targets):
	podman build -t $(prefix)-$@ -f $@.containerfile .

push:
	for name in $(targets); do \
		podman push $(prefix)-$$name quay.io/alesgar/$(prefix)-$$name; \
	done