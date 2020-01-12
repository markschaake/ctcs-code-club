#!/bin/bash

out=/home/pi/Downloads/arch.zip
dest_dir=/home/pi
dest=/home/pi/ctcs-code-club-master
final=/home/pi/code

cleanup() {
  rm -rf "$out"
  rm -rf "$dest"
}

fail() {
  echo "$1" && exit 1
}

if [ -d "$dest" ]; then
  rm -rf "$dest"
  mkdir "$dest"
fi

wget -O "$out" https://github.com/markschaake/ctcs-code-club/archive/master.zip || fail "Could not download archive"
unzip "$out" -d "$dest_dir" || fail "Could not extract to destination"
rm -rf "$final"
mv "$dest" "$final"
chmod +x "${final}/scripts/update.sh"
cleanup && echo "SUCCESS"
