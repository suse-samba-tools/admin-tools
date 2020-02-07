# Build deps: make automake autoconf yast2-buildtools gcc gcc-c++ yast2-devtools dejagnu flex libboost_headers1_66_0-devel jemalloc jemalloc-devel autoconf-archive python3-devel swig docbook-xsl-stylesheets libboost_test1_66_0-devel ncurses-devel ruby-devel
# Module run deps: ruby2.5-rubygem-yast-rake python3-ldap python3-keyring

all:
	pushd yast-core; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd libyui; if [ ! -f Makefile ] ; then make -f Makefile.cvs; cmake CMakeLists.txt; fi; make && sudo make install; popd
	pushd libyui-ncurses; if [ ! -f Makefile ] ; then  make -f Makefile.cvs; cmake CMakeLists.txt; fi; make && sudo make install; popd
	pushd yast-ycp-ui-bindings; if [ ! -f Makefile ] ; then make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd yast-python-bindings; if [ ! -f Makefile ] ; then make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd yast-ruby-bindings; if [ ! -f Makefile ] ; then cmake -DCMAKE_INSTALL_PREFIX=/usr CMakeLists.txt; fi; make && sudo make install; popd
	pushd yast-perl-bindings; if [ ! -f Makefile ] ; then make -f Makefile.cvs; fi; make && sudo make install; popd
	pushd yast-yast2; sudo rake install; popd

install:
	pushd yast-core; make install; popd
	pushd libyui; make install; popd
	pushd libyui-ncurses; make install; popd
	pushd yast-ycp-ui-bindings; make install; popd
	pushd yast-python-bindings; make install; popd

modules:
	pushd yast2-adcommon-python; sudo ./setup.py install; popd
	pushd yast2-aduc; rake install; popd
	pushd yast2-adsi; rake install; popd
	pushd yast2-gpmc; rake install; popd
	pushd yast2-dns-manager; rake install; popd

uninstall:
	pushd yast-python-bindings; make uninstall; popd
	pushd yast-ycp-ui-bindings; make uninstall; popd
	pushd libyui-ncurses; make uninstall; popd
	pushd libyui; make uninstall; popd
	pushd yast-core; make uninstall; popd
