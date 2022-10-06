<!--
SPDX-FileCopyrightText: Nir Soffer <nirsof@gmail.com>
SPDX-License-Identifier: GPL-2.0-or-later
-->

# Contributing to userstorage

Thanks for taking the time to contribute!

This document conforms a set of guidelines for contributing to userstorage.

## Where do I get started?

Make sure to check the [README](README.md). You need to have all
requirements installed, be able to run tests, and understand the project.

## How to contribute?

### Opened Issues

Check the issues that are currently open, as all contributors are always
welcome to post new patches. You can look for the `good first issue`
tag if you are a first time contributor. Also, issues tagged as
`help wanted` represent specially interesting features to implement, but
require a bit more involvement.

### Reporting bugs

If you found a bug, please open an issue, and discuss it before starting
any development. Also, make sure that the bug is not covered already in
another existing issue.

New issues must have good, descriptive titles. And you shall make sure to
include as many details as possible. These details can include, but are
not limited to:
- Detailed description of the issue.
- The exact steps to reproduce (when it makes sense).
- What would be the expected behaviour for the tool.
- How can it be fixed.

New issues for bugs should have the `bug` tag.

### Suggesting enhancements

If you have an idea for improving this tool, please open an issue to
discuss the idea. Remember to check the list of open issues first and write
good, descriptive title and description.

## Making a code contribution

Once you have discussed a new bug or feature, you can start coding.

Fork the project, create a new branch, create new commits, and send
a pull request. Note that for trivial changes, you can still just send a
pull request without an associated Issue.

Do not forget to add upstream as one of your remotes to keep your
local fork updated:
    git remote add git@github.com:nirs/userstorage.git

### Pull Requests

When submitting new PRs, please try to maintain code quality.
Follow the [styleguides](#styleguides).

Before pushing the changes, make sure you have rebased your branch to
the latest upstream master branch:

    git rebase upstream master
    git rebase master
    git push

## Styleguides

### Git commit messages

Commit title should be a short summary under 50 chars (if possible).

The topic should be a module name, a subsystem name, or a feature name,
helping to understand what is this patch about.

The rest of the commit message should include a longer description,
explaining why this patch is needed, why it is implemented in the
specific way, and the nature of the change.

The description should use line length of 72 chars and multiple
paragraphs if necessary.

### Coding style

The coding conventions are generally aligned with the
[PEP 8](https://peps.python.org/pep-0008/) style recommendations.
Code is linted with `flake8` and `pylint` in error mode only.
You can run the linters by doing:

    tox -e flake8,pylint

In general, it is very important for new code to be consistent with the existing
code in the same module, or in the same package for new modules. In case of
doubt, check the already existing code before!