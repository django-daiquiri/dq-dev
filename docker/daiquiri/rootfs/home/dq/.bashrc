alias ..="cd .."
alias env="env | sort"
alias p="python"
alias pm="python ${DQAPP}/manage.py"
alias psa="ps faux"
alias spv="spv.sh"
alias tailf="tail -F"
alias tlp="netstat -tulpen"
alias tlps="sudo netstat -tulpen"
alias we="watchexec"

export LS_COLORS=${LS_COLORS}:"di=1;34":"*.txt=1;36":"*.md=0;93"
alias l="ls --color=auto -CF"
alias ll="ls --color=auto -alF"
alias la="ls --color=auto -AlF"

# the following four functions are abstraction layers using wait_for
# they cover a few typical use cases and serve as inspiration
function wait_for(){
    arg="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:2}"
    fi
    wait_for.sh "${arg}" "${max_wait}" "${command_on_success}"
}

function wait_for_file(){
    file="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:2}"
    fi
    wait_for.sh "cat \"${file}\"" "${max_wait}" "${command_on_success}"
}

function wait_for_folder(){
    folder="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:2}"
    fi
    wait_for.sh "cd \"${folder}\"" "${max_wait}" "${command_on_success}"
}

function wait_for_process(){
    process="${1}"
    pgrep="[${process:0:1}]${process:1:100}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:2}"
    fi
    wait_for.sh "ps aux | grep \"${pgrep}\"" "${max_wait}" "${command_on_success}"
}

function wait_for_url(){
    url="${1}"
    max_wait="${2}"
    command_on_success="${@:3}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:2}"
    fi
    wait_for.sh "curl ${1}" "${max_wait}" "${command_on_success}"
}

function wait_for_caddy(){
    max_wait="${1}"
    command_on_success="${@:2}"
    if [[ -z "${max_wait}" ]]; then
        max_wait=300
        command_on_success="${@:1}"
    fi
    wait_for_process "caddy run --config" "${max_wait}" "${command_on_success}"
}

# examples of how to use the functions above
# wait_for "mkdir /vol/mount" 60 "echo folder exists" &
# wait_for_caddy 30 "echo caddy up"
# wait_for_url localhost:9992 30 "echo port response good"
# wait_for_file /tmp/file 120 "ls -la /tmp/file"
# wait_for_folder /tmp/folder 120 "ls -la /tmp/folder"

cd "${HOME}"
