#!/usr/bin/bash

# set -x
set -eu
set -o pipefail

declare -gr __HERE=$(cd $(dirname $0) && pwd)
declare -gr __FLD_BCKP=${__HERE}/backup

for p in $(incus profile ls -cn -fcsv | grep -v ^default); do
	incus profile show $p | sed -e 's|^- /1.0/instances.*||g;/^$/d' > ${__FLD_BCKP}/profiles/${p}.yml
done

for n in $(incus network ls -cn -fcsv | sed 's/^lo//g;s/enp3s0//g;/^$/d'); do
	incus network show $n | sed 's|^- /1.0/instances.*||g;/^$/d' > ${__FLD_BCKP}/networks/${n}.yml
done

for s in $(incus storage ls -cn -fcsv); do
	incus storage show $s | sed -e 's|^- /1.0/instances.*||g;/^$/d' > ${__FLD_BCKP}/storage/${s}.yml
done
