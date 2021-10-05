#!/bin/bash

caddyfile="${HOME}/Caddyfile"

if [[ -f "${caddyfile}" ]]; then
    caddy run --config "${caddyfile}" --adapter caddyfile --watch
else
    exit 1
fi
