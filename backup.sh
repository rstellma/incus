#!/usr/bin/bash

# set -x
set -eu
set -o pipefail

declare -gr __HERE=$(cd $(dirname $0) && pwd)

for p in $(incus profile ls -cn -fcsv | grep -v ^default); do
	incus profile show $p | sed -e 's|^- /1.0/instances.*||g;/^$/d' > ${__HERE}/profiles/${p}.yml
done

for n in $(incus network ls -cn -fcsv | sed 's/^lo//g;s/enp3s0//g;/^$/d'); do
	incus network show $n | sed 's|^- /1.0/instances.*||g;/^$/d' > ${__HERE}/networks/${n}.yml
done

for s in $(incus storage ls -cn -fcsv); do
	incus storage show $s | sed -e 's|^- /1.0/instances.*||g;/^$/d' > ${__HERE}/storage/${s}.yml
done
