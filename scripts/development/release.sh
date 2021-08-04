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

main(){
  cd "${WORKDIR}"

  VERSION="v$(aziona --version)" 
  
  if [ "$(git ls-remote --tags origin refs/tags/"${VERSION}")" != "" ] ; then
    echo "${VERSION} exist!"
    exit
  fi 

  echo "Deploy new version ${VERSION}"

  git tag "${VERSION}"
  git push --tags
}

main "$@"