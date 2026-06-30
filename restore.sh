#!/usr/bin/bash

#set -x
set -eu
set -o pipefail

declare -gr __HERE=$(cd $(dirname $0) && pwd)

for p in $(ls ${__HERE}/profiles/*.yml); do
	incus profile create $(basename ${p%.*}) < $p
done

for n in $(ls ${__HERE}/networks/*.yml); do
	incus network create $(basename ${n%.*}) < $n
done

for s in $(ls ${__HERE}/storage/*.yml); do
	incus storage create $(basename ${s%.*}) < $s
done
