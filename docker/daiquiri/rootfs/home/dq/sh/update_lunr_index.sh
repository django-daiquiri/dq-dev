#!/bin/bash

mkdir -p "${HOME}/log"

watch=""
if [[ "${1}" == "-w" ]]; then
    watch="-w"
fi

lunr-indexer \
    "${HOME}/content" \
    -o "${HOME}/content/lunr-index.json" \
    -l "${HOME}/log/lunr-indexer.log" \
    -f ${watch}
