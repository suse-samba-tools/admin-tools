AC_INIT([admin-tools], [1.0])
AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE
AC_CONFIG_FILES([src/Makefile src/clients/Makefile])
AC_DEFINE(PREFIX, $(prefix))
AC_DEFINE(LIBDIR, $(libdir))
export PATH=$PATH:${ac_abs_confdir}/src:${ac_abs_confdir}/src/yast-devtools/build-tools/doxygen
ln -fs ../configure src/libyui/configure
ln -fs ./buildtools/CMakeLists.common src/libyui/CMakeLists.txt
ln -fs ../configure src/libyui-ncurses/configure
ln -fs ../libyui/buildtools/CMakeLists.common src/libyui-ncurses/CMakeLists.txt
pushd src/yast-core; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
sed -i 's;SET( BUILDTOOLS_DIR .* );SET( BUILDTOOLS_DIR "'${ac_abs_confdir}'/src/libyui/buildtools" );g' src/libyui/buildtools/CMakeLists.common
AX_SUBDIRS_CONFIGURE([src/yast-core, src/libyui], [PKG_CONFIG_PATH=${ac_abs_confdir}/src])
AX_SUBDIRS_CONFIGURE([src/libyui-ncurses], [CXXFLAGS="-I${ac_abs_confdir}/src", -DCMAKE_MODULE_PATH=${ac_abs_confdir}/src/libyui/buildtools])
pushd src/yast-ycp-ui-bindings; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
ln -fs libyui/src src/yui
AX_SUBDIRS_CONFIGURE([src/yast-ycp-ui-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${ac_abs_confdir}/src, CPPFLAGS="-I${ac_abs_confdir}/src\ -I${ac_abs_confdir}/src/yast-core/libscr/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2util-r/src/include\ -I${ac_abs_confdir}/src/yast-core/libycp/src/include", LDFLAGS="-L${ac_abs_confdir}/src/ycp-ui\ -L${ac_abs_confdir}/src/wfm\ -L${ac_abs_confdir}/src/yast-core/libscr/src\ -L${ac_abs_confdir}/src/yast-core/liby2/src\ -L${ac_abs_confdir}/src/yast-core/liby2util-r/src\ -L${ac_abs_confdir}/src/yast-core/libycp/src\ -L${ac_abs_confdir}/src/libyui/src"])
pushd src/yast-python-bindings; PKG_CONFIG_PATH=${ac_abs_confdir}/src make -f Makefile.cvs all; popd
AX_SUBDIRS_CONFIGURE([src/yast-python-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${ac_abs_confdir}/src, CPPFLAGS="-I${ac_abs_confdir}/src\ -I${ac_abs_confdir}/src/yast-core/libscr/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2/src/include\ -I${ac_abs_confdir}/src/yast-core/liby2util-r/src/include\ -I${ac_abs_confdir}/src/yast-core/libycp/src/include", LDFLAGS="-L${ac_abs_confdir}/src/ycp-ui\ -L${ac_abs_confdir}/src/wfm\ -L${ac_abs_confdir}/src/yast-core/libscr/src\ -L${ac_abs_confdir}/src/yast-core/liby2/src\ -L${ac_abs_confdir}/src/yast-core/liby2util-r/src\ -L${ac_abs_confdir}/src/yast-core/libycp/src", --enable-python3])
AC_OUTPUT
