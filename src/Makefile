# Build deps: make automake autoconf yast2-buildtools gcc gcc-c++ yast2-devtools dejagnu flex libboost_headers1_66_0-devel jemalloc jemalloc-devel autoconf-archive python3-devel swig docbook-xsl-stylesheets libboost_test1_66_0-devel ncurses-devel

all:
	pushd yast-core; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd libyui; if [ ! -f Makefile ] ; then make -f Makefile.cvs; cmake CMakeLists.txt; fi; make && sudo make install; popd
	pushd libyui-ncurses; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; cmake CMakeLists.txt; fi; make && sudo make install; popd
	pushd yast-ycp-ui-bindings; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd yast-python-bindings; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; fi; make && sudo make install; popd

install:
	pushd yast-core; make install; popd
	pushd libyui; make install; popd
	pushd libyui-ncurses; make install; popd
	pushd yast-ycp-ui-bindings; make install; popd
	pushd yast-python-bindings; make install; popd

uninstall:
	pushd yast-python-bindings; make uninstall; popd
	pushd yast-ycp-ui-bindings; make uninstall; popd
	pushd libyui-ncurses; make uninstall; popd
	pushd libyui; make uninstall; popd
	pushd yast-core; make uninstall; popd
