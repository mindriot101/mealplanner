#!/bin/bash

set -eou pipefail

GREEN="\e[32m"
RED="\e[31m"
RESET="\e[0m"
DEPLOY_HOST=pi4
DEPLOY_DIR="apps/mealplanner"

log() {
    echo -e "${GREEN}$1${RESET}" >&2
}

error() {
    echo -e "${RED}$1${RESET}" >&2
}

main() {
    run_main "$@"
}

remote_command() {
    if [[ $# -ne 1 ]]; then
        error "No argument supplied"
        return 1
    fi

    ssh -t ${DEPLOY_HOST} "cd ${DEPLOY_DIR} && $1"
}

run_main() {
    if [[ $# == 1 ]]; then
        local branch=$1
    else
        local branch=main
    fi

    remote_command "git fetch origin"
    remote_command "git checkout origin/$branch"
    remote_command 'docker-compose up --detach --build'
}

main "$@"
