#!/usr/bin/bash

# set -x
set -eu
set -o pipefail

declare -r DESKTOP="${1:-fluxbox}"
declare -r CONTAINER="${2:-desktop}"

[[ -z "$(which Xephyr 2>/dev/null)" ]] && { echo "Nope! No containerized desktop for you. Install 'Xephyr' first."; exit 1; }

# It's a bit "hacky" but it's the only thing we can rely on; 
# the physical interface could be named "eth0," "enp3s0," or something else.
IP="$(ip r s | tail -1 | cut -f9 -d' ')"
readonly IP

declare -i found_free_socket=0
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
	if ! ss -lx | grep -q /tmp/.X11-unix/X"${socket}"; then
		found_free_socket=1
		break
	fi
done
[[ $found_free_socket -eq 0 ]] && exit 1	# Apparently, 10 desktop sessions weren't enough.

if ! incus info "$CONTAINER" | grep -q "Status: RUNNING"; then
	incus start "$CONTAINER"
	res=$?
fi
[[ $res -ne 0 ]] && exit $res

Xephyr :"${socket}" -screen 1900x1024 -ac -br -nolisten unix -listen tcp &
res=$?
[[ $res -ne 0 ]] && exit $res


incus exec "$CONTAINER" -- sudo -u "$USER" env DISPLAY="${IP}:${socket}" "$cmd" &
