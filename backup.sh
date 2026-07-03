#!/usr/bin/bash

# set -x
set -eu
set -o pipefail

__HERE=$(cd "$(dirname "$0")" && pwd)
readonly __HERE



for p in $(incus profile ls -cn -fcsv | grep -v ^default); do
	incus profile show "$p" > "${__HERE}"/profiles/"${p}".yml
done

for n in $(incus network ls -cn -fcsv | sed '/^lo/d;/enp3s0/d'); do
	incus network show "$n" > "${__HERE}"/networks/"${n}".yml
done

for s in $(incus storage ls -cn -fcsv); do
	incus storage show "$s" > "${__HERE}"/storage/"${s}".yml
done

for i in $(incus ls type=container -cn -fcsv); do
	echo -e "[INFO] Container '\033[1;36m$i\033[1;0m'"
	incus config show "$i" > "${__HERE}"/instances/"${i}".yml
	incus export "$i" "${__HERE}"/instances/"${i}".tar.gz
done
