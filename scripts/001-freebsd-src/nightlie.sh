#!/usr/bin/env zsh

dataset="tank/src/freebsd"

directory=$(zfs get -H -ovalue mountpoint ${dataset})

cd ${directory}

git fetch upstream-github

git merge upstream-github/master

git push origin soldierx/lattera/aslr
