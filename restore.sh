#!/usr/bin/bash

#set -x
set -eu
set -o pipefail

__HERE=$(cd "$(dirname "$0")" && pwd)
readonly __HERE



for p in "${__HERE}"/profiles/*.yml; do
	incus profile create "$(basename "${p%.*}")" < "$p"
done

for n in "${__HERE}"/networks/*.yml; do
	incus network create "$(basename "${n%.*}")" < "$n"
done

for s in "${__HERE}"/storage/*.yml; do
	incus storage create "$(basename "${s%.*}")" < "$s"
done

for i in "${__HERE}"/instances/*.tar.gz; do
	incus import "$i" "$(basename "${i%%.*}")"
	# This step is only successful if an instance with
	# the same network interface does not already exist.
	# Otherwise, it fails with:
	# > "Error: Failed start validation for device "eth0":
	# > MAC address "foobar" already defined on another NIC"
	incus start "$(basename "${i%%.*}")"
done
