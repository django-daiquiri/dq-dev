#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
basedir=$(echo "${scriptdir}" | grep -Po ".*(?=/)")
profdir="${basedir}/usr/profiles"
active_yaml="${profdir}/active.toml"
spacer="\t::\t"
cd "${basedir}"

function short_cmd() {
    op=$(echo "${cmd}" | sed "s/python manage.py //g")
    if (("${#op}" < 3)); then
        op="prof exists"
    fi
    echo "${op}"
}

function fail() {
    echo -e "\033[0;91m[FAIL]\033[0m $(short_cmd)${spacer}${rx}"
    failed="true"
}

function pass() {
    echo -e "\033[0;32m[PASS]\033[0m $(short_cmd)${spacer}${rx}"
}

function remove_profile() {
    fulldir="${profdir}/${1}"
    if [[ (-n "${1}" && -d "${fulldir}") ]]; then
        rm -rf "${fulldir}"
    fi
}

function test() {
    failed="false"
    cmd="python manage.py ${1}"
    rx="${2}"
    eval "${cmd}" | grep -Poi "${rx}" >/dev/null 2>&1 || fail
    if [[ "${failed}" == "false" ]]; then
        pass
    fi
}

# main
active_yaml_before="$(cat "${active_yaml}")"

prof1="test_prof1"
prof2="test_prof2"
remove_profile "${prof1}"
remove_profile "${prof2}"

test "-c ${prof1}" "fresh profile.*${prof1}.*created"
test "" "${prof1}"

test "-c ${prof2}" "fresh profile.*${prof2}.*created"
test "" "${prof2}"
test "-s ${prof1}" "set active profile.*${prof1}"
test "" "${prof1}.*\*.*\*"
test "-s ${prof2}" "set active profile.*${prof2}"
test "" "${prof2}.*\*.*\*"

test "-e none -n" "profile.*none.*does not seem to exist"
test "-e" "/${prof2}/docker-compose.yaml"
test "-e ${prof1}" "/${prof1}/docker-compose.yaml"
remove_profile "${prof1}"
remove_profile "${prof2}"

echo "${active_yaml_before}" >"${active_yaml}"
