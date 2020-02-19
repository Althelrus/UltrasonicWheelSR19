#!/bin/sh
git config --global alias.up '!git remote update -p; git merge --ff-only @{u}'
for repo in repo1 repo2 repo3 repo4; do
    (cd "${repo}" && git checkout master && git up)
done