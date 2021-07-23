#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."
TEST=${TEST:-"false"}

main(){
  if [ -z ${1} ] ; then
    OUTPUT_PATH="/tmp/aziona-dist.tar.gz" 
  else
    OUTPUT_PATH=${1}
  fi

  cd ${WORKDIR}

  pip3 install --upgrade virtualenv
  
  mkdir -pv venv
  
  python3 -m virtualenv venv
  
  . ./venv/bin/activate 

  pip3 install -e . 

  # lint & test
  if [ ${TEST} == "true" ] ; then
    pip3 install -r requirements-dev.txt
    black aziona
    flake8 aziona
    isort aziona
    python3 setup.py test
  fi
  
  # build
  python3 setup.py clean build

  echo "Build artifact in: ${OUTPUT_PATH}"
  tar -czvf aziona-dist.tar.gz dist
  cp aziona-dist.tar.gz ${OUTPUT_PATH}
}

main "$@"