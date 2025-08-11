#!/bin/bash
echo "wait_for.sh started at $(date)"

check_cmd="${1}"
max_wait="${2}"
command_on_success="${@:3}"
if [[ -z "${max_wait}" ]]; then
    max_wait=300
    command_on_success="${@:2}"
fi

# wait_for is a generic function that can be used to wait for a command
# to finish with exit code 0
# it can take up to three args, the first is required the others are optional
# look at the functions further below which illustrate the usage of wait_for
c=0
echo "Wait for success of \"${check_cmd}\", max wait ${max_wait}s"
while true; do
    c=$((c + 1))
    eval "${check_cmd}" >/dev/null 2>&1 && break
    if (("${c}" > "${max_wait}")); then
        echo "Exit because max wait reached for \"${check_cmd}\""
        exit 1
    fi
    sleep 1
done
printf "Success calling \"${check_cmd}\""
if [[ -n "${command_on_success}" ]]; then
    echo ", run on success \"${command_on_success}\""
    eval "${command_on_success}"
fi
exit 0
