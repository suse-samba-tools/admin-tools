#!/bin/bash

ac_abs_confdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
for i in NEWS README AUTHORS ChangeLog; do
	if [ ! -f ${ac_abs_confdir}/${i} ] ; then
		touch ${ac_abs_confdir}/${i}
	fi
done
sed 's;@TOP_SRiC_DIR@;'${ac_abs_confdir}';g' ${ac_abs_confdir}/src/yast-ruby-bindings.make.in > ${ac_abs_confdir}/src/yast-ruby-bindings/Makefile.am && autoreconf -if
