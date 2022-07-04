#!/bin/bash
IFS=$'\n'
source_basepy="${HOME}/app/config/settings/base.py"
source_spv_tpl="${HOME}/tpl/supervisord.conf"
target_spv_conf="${HOME}/conf/supervisord.conf"
tempfile="/tmp/spv_conf.tmp"

piddir="${HOME}/run"
logdir="${HOME}/log"

function printerr() {
    echo -e "\033[0;91mError parsing supervisord conf template"
    exit 1
}

function extract_query_queues_entry() {
    echo $(cat ${source_basepy}) |
        grep -Po "(?<=QUERY_QUEUES).*\]" |
        sed "s|=||g" | sed "s|'|\"|g" | jq >"${tempfile}"
    jq . "${tempfile}" >/dev/null 2>&1 || printerr
}

function get_list_entry() {
    jq -r ".[${2}].${1}" "${tempfile}"
}

function sanitize_string() {
    echo "${1}" | tr '[:upper:]' '[:lower:]' | sed "s|[^a-z0-9_-]|_|g"
}

function ap() {
    if [[ -n "${1}" ]]; then
        echo -e "${1}" >>"${target_spv_conf}"
    fi
}

# main
cat "${source_spv_tpl}" >"${target_spv_conf}"

if [[ "$(echo ${ASYNC} | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    extract_query_queues_entry
    key_no=$(cat "${tempfile}" | grep -c "{")

    ap "\n\n# automatically created query queue calls"

    for ((i = 0; i < ${key_no}; i++)); do
        key="$(get_list_entry "key" ${i})"
        san="$(sanitize_string ${key})"
        ap "\n[program:query_${san}]"
        ap "command = run-rmq-worker.sh query_${key} 2"
        ap "exitcodes = 255"
    done
fi
ap ""

if [[ -n "${ADD_TO_SUPERVISORD_CONF}" ]]; then
    ap "\n\n# added custom service(s) from conf.toml\n"

    arr=($(echo "${ADD_TO_SUPERVISORD_CONF:1:-1}" | sed 's|, |\n|g'))
    for el in "${arr[@]}"; do
        ap "${el:1:-1}"
    done
fi
ap "\n"