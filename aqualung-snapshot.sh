#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "${tmp}" -o ! -d "${tmp}" ] || rm -rf "${tmp}"
}

unset CDPATH
pwd="$(pwd)"
tmp_dirname=aqualung-export

cd "${tmp}"
svn co \
   https://aqualung.svn.sourceforge.net/svnroot/aqualung/trunk "${tmp_dirname}"
cd "${tmp_dirname}"

svn=$(LC_ALL=C svn info 2> /dev/null | grep Revision | cut -d' ' -f2)
echo "#define AQUALUNG_VERSION \"R-${svn}\"" > src/version.h
find . -type d -name .svn -print0 | xargs -0r rm -rf
cd ..
dirname="${tmp_dirname}-r${svn}"
mv "$tmp_dirname" "$dirname"

tar fjc "$pwd"/"${dirname}".tar.bz2 "${dirname}"
cd "${dirname}" >/dev/null

