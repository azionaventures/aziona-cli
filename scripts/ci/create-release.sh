#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail
set -o nounset

showHelp() {
   echo "Esecuzione container all'interno del pod"
   echo
   echo "Syntax: setup.sh [ -v;--version | -h;--help ]"
   echo "options:"
   echo "-h | --help            : Print help"
   echo "-v | --version         : New version"
   echo
}


WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."
VERSION_FILEPATH="aziona/__init__.py"

parser() {
  options=$(getopt -l "help,version:,yes" -o "h v: y:" -a -- "$@")
  eval set -- "$options"

  while true
      do
      case $1 in
          -h|--help)
              showHelp 
              exit 0
              ;;
          -v|--version)
              VERSION="${2}"
              ;;
          -y|--yes)
              CONFIRM="y"
              ;;
          --)
              shift
              break;;
      esac
      shift
  done
  shift "$(($OPTIND -1))"

  if [ -z "${VERSION:-}" ] ; then
    read -p "Input new version (only -> x.y.z): " VERSION
  fi
  VERSION_NAME="v${VERSION}"
}

main(){
  cd "${WORKDIR}"

  if [ "main" != "$(git branch --show-current)" ] ; then
    echo "[WARNING] BRANCH IS NOT MAIN: $(git branch --show-current)"
  fi

  echo "Latest release: $(git ls-remote --tags origin | tail -1 | cut -d / -f 3)"

  parser "$@"

  if [ "$(git ls-remote --tags origin refs/tags/${VERSION_NAME})" != "" ] ; then
    echo "Tag version ${VERSION} exist!"
    exit 1
  fi 

  if [[ ${VERSION} =~ ^[0-9]+(\.[0-9]+){2,3}$ ]] ; then
    echo "Deploy new version ${VERSION}"

    echo "__version__ = \"${VERSION}\"" > ${VERSION_FILEPATH}

    git diff ${VERSION_FILEPATH}

    if [ -z "${CONFIRM:-}" ] ; then
      read -p "Release version ${VERSION_NAME}. Are you sure? (y or n) " CONFIRM
    fi
    if [[ ${CONFIRM} =~ ^[Yy]$ ]]
    then
      git add  ${VERSION_FILEPATH}
      #git commit -m "Release version: ${VERSION_NAME} \n\nCommit hash: $(git rev-parse --short HEAD)"
      #git tag "${VERSION_NAME}"
      #git push origin "${VERSION_NAME}"
      #git push
      echo "New release ${VERSION} pushed"
    fi
  else
    echo "Error release number. Expect x.y.z ex. 1.2.3"
  fi
}

main "$@"