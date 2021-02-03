#!/bin/bash

ac_abs_confdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
for i in NEWS README AUTHORS ChangeLog; do
	if [ ! -f ${ac_abs_confdir}/${i} ] ; then
		touch ${ac_abs_confdir}/${i}
	fi
done
patch -d ${ac_abs_confdir}/src/libyui-ncurses -p1 < ${ac_abs_confdir}/src/find_curses.patch
sed 's;@TOP_SRC_DIR@;'${ac_abs_confdir}';g' ${ac_abs_confdir}/src/yast-ruby-bindings.make.in > ${ac_abs_confdir}/src/yast-ruby-bindings/Makefile.am && autoreconf -if
