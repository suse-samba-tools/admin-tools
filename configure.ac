AC_INIT([admin-tools], [1.0])
AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE
AX_PYTHON_DEVEL
AX_PKG_SWIG([], [], AC_MSG_ERROR([SWIG is required to build.]))
AX_SWIG_PYTHON
AC_PROG_CXX
AC_CONFIG_FILES([src/Makefile])
AC_CONFIG_COMMANDS([yast-core], [pushd src/yast-core; make -f Makefile.cvs; popd])
AC_CONFIG_COMMANDS([libyui], [pushd src/libyui; make -f Makefile.cvs; cmake CMakeLists.txt; popd])
AC_CONFIG_COMMANDS([libyui-ncurses], [pushd src/libyui-ncurses; make -f Makefile.cvs; cmake CMakeLists.txt; popd])
AC_CONFIG_COMMANDS([yast-ycp-ui-bindings], [pushd src/yast-ycp-ui-bindings; CPPFLAGS="-I../../yast-core/libscr/src/include -I../../yast-core/liby2/src/include -I../../yast-core/liby2util-r/src/include -I../../yast-core/libycp/src/include" LDFLAGS="-L../../yast-core/libscr/src -L../../yast-core/liby2/src -L../../yast-core/liby2util-r/src -L../../yast-core/libycp/src" make -f Makefile.cvs; popd])
AC_CONFIG_COMMANDS([yast-python-bindings], [pushd src; ln -s yast-ycp-ui-bindings/src ycp-ui; ln -s yast-core/wfm/src wfm; popd; pushd src/yast-python-bindings; make -f Makefile.cvs all && CPPFLAGS="-I../.. -I../../yast-core/libscr/src/include -I../../yast-core/liby2/src/include -I../../yast-core/liby2util-r/src/include -I../../yast-core/libycp/src/include" LDFLAGS="-L../../yast-core/libscr/src -L../../yast-core/liby2/src -L../../yast-core/liby2util-r/src -L../../yast-core/libycp/src" ./configure --enable-python3; popd])
AC_CONFIG_COMMANDS([yast-ruby-bindings], [pushd src/yast-ruby-bindings; cmake -DCMAKE_INCLUDE_PATH=../yast-core/libscr/src/include:../yast-core/liby2/src/include:../yast-core/liby2util-r/src/include:../yast-core/libycp/src/include:../yast-core/libycp/testsuite/tests/include -DCMAKE_INSTALL_PREFIX=/usr CMakeLists.txt; popd])
AC_OUTPUT
