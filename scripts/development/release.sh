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
VERSION_FILEPATH="aziona/__init__.py"

main(){
  cd "${WORKDIR}"
  
  echo "Latest release: v$(aziona --version)"

  read -p "Input new version (x.y.z): " VERSION
  VERSION="${VERSION}"
  VERSION_NAME="v${VERSION}"
  
  if [ "$(git ls-remote --tags origin refs/tags/${VERSION_NAME})" != "" ] ; then
    echo "${VERSION} exist!"
    exit 1
  fi 

  if [[ ${VERSION} =~ ^[0-9]+(\.[0-9]+){2,3}$ ]] ; then
    echo "Deploy new version ${VERSION}"

    echo "__version__ = \"${VERSION}\"" > ${VERSION_FILEPATH}

    git diff ${VERSION_FILEPATH}

    read -p "Release version ${VERSION_NAME}. Are you sure? (y,yes or n, no) " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      git add  ${VERSION_FILEPATH}
      git commit -m "Release version: ${VERSION_NAME} \n\nCommit hash: $(git rev-parse --short HEAD)"
      git tag "${VERSION_NAME}"
      git push --tags
      echo "New release ${VERSION} pushed"
    fi
  else
    echo "Error release number. Expect x.y.z ex. 1.2.3"
  fi
}

main "$@"