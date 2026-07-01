#!/usr/bin/bash

# set -x
set -eu
set -o pipefail

declare -gr __HERE=$(cd $(dirname $0) && pwd)



for p in $(incus profile ls -cn -fcsv | grep -v ^default); do
	incus profile show $p > ${__HERE}/profiles/${p}.yml
done

for n in $(incus network ls -cn -fcsv | sed '/^lo/d;/enp3s0/d'); do
	incus network show $n > ${__HERE}/networks/${n}.yml
done

for s in $(incus storage ls -cn -fcsv); do
	incus storage show $s > ${__HERE}/storage/${s}.yml
done

for i in $(incus ls -cn -fcsv); do
	incus config show $i > ${__HERE}/instances/${i}.yml
	incus export $i ${__HERE}/instances/${i}.tar.gz
done
