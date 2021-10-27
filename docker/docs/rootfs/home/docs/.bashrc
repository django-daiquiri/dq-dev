alias ..="cd .."
alias env="env | sort"
alias tlp="netstat -tulpen"
alias ll="ls -lah"
alias psa='function _psa(){ if [[ -n "${1}" ]]; then ps faux | rg "${1}" | rg -v "rg --pcre2.*${1}"; else ps faux; fi };_psa'
alias tailf="tail -F"

cd "${HOME}"
