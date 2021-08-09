#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

main(){
  cd "${WORKDIR}"

  if [ -n "${1:-}" ] ; then
    docker build -f Dockerfile --build-arg AZIONA_CLI_VERSION="${1}" .
  else
    docker build -f Dockerfile .
  fi
}

main "$@"