AC_INIT([admin-tools], [1.0])
AC_PREFIX_DEFAULT(/usr)
AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE
sed 's;@TOP_SRC_DIR@;'${ac_abs_confdir}';g' ${ac_abs_confdir}/src/yast-ruby-bindings.make.in > ${ac_abs_confdir}/src/yast-ruby-bindings/Makefile.am && autoreconf -if
AC_CONFIG_FILES([Makefile src/Makefile src/clients/Makefile src/yast-ruby-bindings/Makefile])
AC_DEFINE(PREFIX, $(prefix))
AC_DEFINE(LIBDIR, $(libdir))
export PATH=$PATH:${ac_abs_confdir}/src:${ac_abs_confdir}/src/yast-devtools/build-tools/doxygen
sed 's;\.\.;'${ac_abs_confdir}'/src;g' ${ac_abs_confdir}/src/YastConfig.cmake.in > ${ac_abs_confdir}/src/YastConfig.cmake
sed 's/__attribute__ ((deprecated)) //g' ${ac_abs_confdir}/src/yast-core/libycp/src/include/ycp/YCPMap.h > ${ac_abs_confdir}/src/yast-python-bindings/src/YCPMap.h
ln -fs ../libyui_configure src/libyui/configure
ln -fs ../libyui_makefile src/libyui/Makefile
ln -fs yast-core/wfm/src src/wfm
ln -fs yast-ycp-ui-bindings/src src/ycp-ui
ln -fs yast-core/scr/src src/scr
pushd src/yast-core; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
AX_SUBDIRS_CONFIGURE([src/yast-core, src/libyui], [PKG_CONFIG_PATH=${ac_abs_confdir}/src])
pushd src/yast-ycp-ui-bindings; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
ln -fs libyui/libyui/src src/yui
AX_SUBDIRS_CONFIGURE([src/yast-ycp-ui-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${ac_abs_confdir}/src, CPPFLAGS="-I${ac_abs_confdir}/src\ -I${ac_abs_confdir}/src/yast-core/libscr/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2util-r/src/include\ -I${ac_abs_confdir}/src/yast-core/libycp/src/include", LDFLAGS="-L${ac_abs_confdir}/src/ycp-ui\ -L${ac_abs_confdir}/src/wfm\ -L${ac_abs_confdir}/src/yast-core/libscr/src\ -L${ac_abs_confdir}/src/yast-core/liby2/src\ -L${ac_abs_confdir}/src/yast-core/liby2util-r/src\ -L${ac_abs_confdir}/src/yast-core/libycp/src\ -L${ac_abs_confdir}/src/libyui/libyui/build/src"])
pushd src/yast-python-bindings; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
AX_SUBDIRS_CONFIGURE([src/yast-python-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${ac_abs_confdir}/src, CPPFLAGS="-I${ac_abs_confdir}/src\ -I${ac_abs_confdir}/src/yast-core/libscr/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2util-r/src/include\ -I${ac_abs_confdir}/src/yast-core/libycp/src/include", LDFLAGS="-L${ac_abs_confdir}/src/ycp-ui\ -L${ac_abs_confdir}/src/wfm\ -L${ac_abs_confdir}/src/yast-core/libscr/src\ -L${ac_abs_confdir}/src/yast-core/liby2/src\ -L${ac_abs_confdir}/src/yast-core/liby2util-r/src\ -L${ac_abs_confdir}/src/yast-core/libycp/src", --enable-python3])
AC_OUTPUT
