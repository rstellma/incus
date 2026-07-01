#!/usr/bin/bash

set -x
set -eu
set -o pipefail

declare -r DESKTOP="${1:-fluxbox}"
declare -r CONTAINER="${2:-desktop}"

# It's a bit "hacky" but it's the only thing we can rely on; 
# the physical interface could be named "eth0," "enp3s0," or something else.
declare -r IP="$(ip r s | tail -1 | cut -f9 -d' ')"

declare -i found_Free_socket=0
declare -i res=0

case $DESKTOP in
	"kde"|"plasma"|"plasma6")	cmd="/usr/bin/startplasma-x11";;
	"fluxbox")			cmd="/usr/bin/startfluxbox";;
	*)				cmd="/usr/bin/startfluxbox";;
esac

# 10 desktop sessions should probably be enough.
for socket in {1..10}; do
	# We cannot rely on /var/.X11-unix: there can also be abstract sockets.
	# 'ss' also displays abstract sockets und grep matches "@/var/.X11-unix/X1" as well
	[[ -z "$(ss -lx | grep /tmp/.X11-unix/X${socket})" ]] && { found_free_socket=1; break; }
done
[[ $found_free_socket -eq 0 ]] && exit 1	# Apparently, 10 desktop sessions weren't enough.

[[ -z "$(incus ls status=running | grep $CONTAINER)" ]] && { incus start $CONTAINER; res=$?; }
[[ $res -ne 0 ]] && exit $res

Xephyr :${socket} -screen 1900x1024 -ac -br -nolisten unix -listen tcp &
res=$?
[[ $res -ne 0 ]] && exit $res


incus exec "$CONTAINER" -- sudo -u $USER env DISPLAY="${IP}:${socket}" $cmd &
