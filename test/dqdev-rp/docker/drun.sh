#!/bin/bash

tmpfil="/tmp/caddy.tar.gz"
tfol="/bin"

caddy_bin_url="https://github.com/$(
    curl -Ls "https://github.com/caddyserver/caddy/releases/latest" |
        grep -Po "(?<=href\=\").*linux_amd64\.tar.gz?(?=\")"
)"

mkdir -p "${tfol}"
curl -Ls ${caddy_bin_url} -o "${tmpfil}" &&
    tar xf "${tmpfil}" -C "${tfol}"

caddy run --watch
