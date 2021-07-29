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
TEST=${TEST:-"false"}

main(){
  cd ${WORKDIR}

  # lint & test
  if [ ${TEST} == "true" ] ; then
    pip install -r requirements-dev.txt
    black aziona
    flake8 aziona
    isort aziona
    python3 setup.py test
  fi
  
  # build
  python3 setup.py clean build
}

main "$@"