alias env="env | sort"
alias p="python"
alias pm="python manage.py"
alias psa="ps faux"
alias tailf="tail -F"
alias tlp="netstat -tulpen"
alias tlps="sudo netstat -tulpen"
alias we="watchexec"
alias wp="wp --path=${WORDPRESS_PATH}"

export LS_COLORS=${LS_COLORS}:"di=1;34":"*.txt=1;36":"*.md=0;93"
alias l="ls --color=auto -CF"
alias ll="ls --color=auto -alF"
alias la="ls --color=auto -A"

# wait_for is a generic function that can be used to wait for a command
# to finish with exit code 0
# it can take up to three args, the first is required the others are optional
# look at the functions further below which illustrate the usage of wait_for
function wait_for(){
    check_cmd="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=120
    fi
    c=0
    echo "Wait for success of \"${check_cmd}\", max wait ${max_wait}s"
    while true; do
        c=$((c+1))
        eval "${check_cmd}" >/dev/null 2>&1 && break
        if (( "${c}" > "${max_wait}" )); then
            echo "Exit because max wait reached for \"${check_cmd}\""
            return
        fi
        sleep 1
    done
    printf "Success calling \"${check_cmd}\""
    if [[ -n "${command_on_success}" ]]; then
        echo ", run \"${command_on_success}\""
        eval "${command_on_success}"
    else
        echo ""
    fi
}

# the following four functions are abstraction layers using wait_for
# they cover a few typical use cases and serve as inspiration
function wait_for_caddy(){
    max_wait="${1}"
    command_on_success="${@:2}"
    wait_for "pgrep caddy" "${max_wait}" "${command_on_success}"
}

function wait_for_file(){
    file="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    wait_for "cat \"${file}\"" "${max_wait}" "${command_on_success}"
}

function wait_for_folder(){
    folder="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    wait_for "cd \"${folder}\"" "${max_wait}" "${command_on_success}"
}

function wait_for_url(){
    url="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    wait_for "curl ${1}" "${max_wait}" "${command_on_success}"
}

# examples of how to use the functions above
# wait_for "mkdir /vol/mount" 60 "echo folder exists"
# wait_for_caddy 30 "echo caddy up"
# wait_for_url localhost:9992 30 "echo port response good"
# wait_for_file /tmp/file 120 "ls -la /tmp/file"
# wait_for_folder /tmp/folder 120 "ls -la /tmp/folder"

cd "${HOME}"
