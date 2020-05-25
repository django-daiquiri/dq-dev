#!/bin/bash

function clone() {
    url="${1}"
    fol="${2}"
    if [[ ! -d "${fol}" ]]; then
        echo "Clone ${url}"
        git clone "${url}" "${fol}"
    fi
}

function maybe_copy() {
    source_file="${1}"
    target_file="${2}"
    if [[ "${3}" == "sudo" ]]; then
        cmd="sudo cp -f"
    else
        cmd="cp -f"
    fi
    if [[ ! -f "${target_file}" ]]; then
        cmd="${cmd} \"${source_file}\" \"${target_file}\""
        echo "${cmd}"
        eval "${cmd}"
    fi
}

function get_container_ip() {
    hostname -I | awk '{print $1}'
}

function replace_in_wpconfig() {
    str="${1}"
    rep="${2}"
    wpc="${WP}/wp-config.php"
    echo "Replace in file ${wpc}, ${str} -> ${rep}"
    sed -i "s|\('${str}',\s\).*)|\1'${rep}'\)|g" "${wpc}"
}

function replace_ip_in_vhost() {
    dqip="$(get_container_ip):80"
    echo "Replace of file /etc/apache2/sites-enabled/vhost2.conf"
    sudo sed -i "s|http://[.0-9a-z:]*|http://${dqip}|g" "/etc/apache2/sites-enabled/vhost2.conf"
}
