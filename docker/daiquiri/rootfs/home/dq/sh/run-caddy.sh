#!/bin/bash

if [[ -f "${CADDYFILE}" ]]; then
    caddy run --config "${CADDYFILE}" --adapter caddyfile --watch
else
    exit 1
fi