#!/bin/sh
set -e

cmake_common="../libyui/buildtools/CMakeLists.common"
cmake_target="./CMakeLists.txt"

echo "checking for $cmake_common..."

if [ -f "$cmake_common" ]
then
  ln -fs "$cmake_common" "$cmake_target"
  echo "OK: linked to `pwd`/$cmake_target."
else
  echo "  Use must have libyui(-devel) >= 3.0.4 installed"
  echo "  in \"$prefix\" first !!!"
  exit 1
fi

exit 0
