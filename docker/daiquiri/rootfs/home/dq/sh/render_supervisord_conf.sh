#!/bin/bash
IFS=$'\n'
source_base_py="${HOME}/app/config/settings/base.py"
source_spv_tpl="${HOME}/tpl/supervisord.conf"
target_spv_conf="${HOME}/conf/supervisord.conf"
tempfile="/tmp/spv_conf.tmp"

function printerr() {
    echo -e "\033[0;91mError parsing supervisord conf template"
    exit 1
}

function get_list_entry() {
    jq -r ".[${2}].${1}" "${tempfile}"
}

function random_string() {
    tr -dc "A-Za-z0-9" </dev/urandom | head -c 16
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
sed -i "s/<PASSWORD>/$(random_string)/g" "${source_spv_tpl}"
sed -i "s/<USERNAME>/$(random_string)/g" "${source_spv_tpl}"
envsubst <"${source_spv_tpl}" >"${target_spv_conf}"

if [[ "$(echo "${ASYNC}" | tr '[:upper:]' '[:lower:]')" == "true" ]]; then
    grep -Poz "(?<=QUERY_QUEUES)(.|\n)*?]\n" "${source_base_py}" |
        grep -Poz "[^ \n]" |
        sed "s|\x00||g" |
        sed "s|'|\"|g" |
        sed -e "s|^=\[|[|g" |
        sed -e "s|},\]|}]|g" |
        jq >"${tempfile}"
    jq . "${tempfile}" >/dev/null 2>&1 || printerr

    key_no="$(grep -c "{" "${tempfile}")"

    ap "\n\n# automatically created query queue calls"

    for ((i = 0; i < "${key_no}"; i++)); do
        key="$(get_list_entry "key" "${i}")"
        san="$(sanitize_string "${key}")"
        ap "\n[program:query_${san}]"
        ap "command = run-rmq-worker.sh query_${key} 2"
        ap "exitcodes = 255"
    done
fi
ap ""

if [[ -n "${ADD_TO_SUPERVISORD_CONF}" ]]; then
    ap "\n\n# added custom service(s) from conf.toml\n"

    mapfile -t arr < <(
        echo "${ADD_TO_SUPERVISORD_CONF:1:-1}" | sed 's|, |\n|g'
    )
    for el in "${arr[@]}"; do
        ap "${el:1:-1}"
    done
fi
ap "\n"
