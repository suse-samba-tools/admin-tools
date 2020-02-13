AC_INIT([admin-tools], [1.0])
AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE
AC_CONFIG_FILES([src/Makefile src/clients/Makefile])
AC_DEFINE(PREFIX, $(prefix))
AC_DEFINE(LIBDIR, $(libdir))
export PATH=$PATH:..:../yast-devtools/build-tools/doxygen
ln -fs ../configure src/libyui/configure
ln -fs ./buildtools/CMakeLists.common src/libyui/CMakeLists.txt
ln -fs ../configure src/libyui-ncurses/configure
ln -fs ../libyui/buildtools/CMakeLists.common src/libyui-ncurses/CMakeLists.txt
pushd src/yast-core; PKG_CONFIG_PATH=.. make -f Makefile.cvs all; popd
sed -i 's;SET( BUILDTOOLS_DIR .* );SET( BUILDTOOLS_DIR "../libyui/buildtools" );g' src/libyui/buildtools/CMakeLists.common
AX_SUBDIRS_CONFIGURE([src/yast-core, src/libyui], [PKG_CONFIG_PATH=..])
AX_SUBDIRS_CONFIGURE([src/libyui-ncurses], [CXXFLAGS="-I../..", -DCMAKE_MODULE_PATH=../libyui/buildtools])
pushd src/yast-ycp-ui-bindings; PKG_CONFIG_PATH=.. make -f Makefile.cvs all; popd
ln -fs libyui/src src/yui
AX_SUBDIRS_CONFIGURE([src/yast-ycp-ui-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:.., CPPFLAGS="-I..\ -I../..\ -I../../yast-core/libscr/src/include\ -I../../yast-core/liby2/src/include\ -I../../yast-core/liby2util-r/src/include\ -I../../yast-core/libycp/src/include", LDFLAGS="-L../../ycp-ui\ -L../../wfm\ -L../../yast-core/libscr/src\ -L../../yast-core/liby2/src\ -L../../yast-core/liby2util-r/src\ -L../../yast-core/libycp/src\ -L../../libyui/src"])
pushd src/yast-python-bindings; PKG_CONFIG_PATH=.. make -f Makefile.cvs all; popd
AX_SUBDIRS_CONFIGURE([src/yast-python-bindings], [PKG_CONFIG_PATH=$PKG_CONFIG_PATH:.., CPPFLAGS="-I..\ -I../..\ -I../../yast-core/libscr/src/include\ -I../../yast-core/liby2/src/include\ -I../../yast-core/liby2util-r/src/include\ -I../../yast-core/libycp/src/include", LDFLAGS="-L../../ycp-ui\ -L../../wfm\ -L../../yast-core/libscr/src\ -L../../yast-core/liby2/src\ -L../../yast-core/liby2util-r/src\ -L../../yast-core/libycp/src", --enable-python3])
AC_OUTPUT
