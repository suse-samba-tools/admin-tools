SUBDIRS = yast-core libyui libyui-ncurses clients

all: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

.PHONY: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

yast-ycp-ui-bindings:
	pushd $@; $(MAKE) DEVTOOLSBINDIR=../../yast-core/base/tools/devtools; popd

yast-python-bindings:
	sed 's/__attribute__ ((deprecated)) //g' $(srcdir)/yast-core/libycp/src/include/ycp/YCPMap.h > yast-python-bindings/src/YCPMap.h
	pushd $@; $(MAKE); popd

yast-ruby-bindings:
	ln -s $(srcdir)/yast-core/scr/src $(srcdir)/scr; pushd $@; cmake -DCMAKE_CXX_FLAGS="-I../../../yast-core/liby2util-r/src/include -I../../../yast-core/libycp/src/include -I../../../yast-core/libscr/src/include -I../../.." -DCMAKE_PREFIX_PATH=../ -DCMAKE_INSTALL_PREFIX=$(prefix) CMakeLists.txt && $(MAKE) --trace; popd

clean-local:
	pushd yast-ycp-ui-bindings; $(MAKE) clean; popd
	pushd yast-python-bindings; $(MAKE) clean; popd
	pushd yast-ruby-bindings; $(MAKE) clean; popd

install-exec-hook:
	pushd yast-ycp-ui-bindings; $(MAKE) install; popd
	pushd yast-python-bindings; $(MAKE) install; popd
	pushd yast-ruby-bindings; $(MAKE) install; popd
	pushd yast-rake; rake install; popd
	pushd yast-yast2; rake install; popd
	pushd yast2-adcommon-python; ./setup.py install; popd
	pushd yast2-adsi; rake install; popd
	pushd yast2-aduc; rake install; popd
	pushd yast2-dns-manager; rake install; popd
	pushd yast2-gpmc; rake install; popd

CLEANFILES = ycp-ui wfm scr yui
