SUBDIRS = yast-core libyui libyui-ncurses

all: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

.PHONY: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

yast-ycp-ui-bindings:
	pushd $@; $(MAKE) DEVTOOLSBINDIR=../../yast-core/base/tools/devtools; popd

yast-python-bindings:
	sed 's/__attribute__ ((deprecated)) //g' $(srcdir)/yast-core/libycp/src/include/ycp/YCPMap.h > yast-python-bindings/src/YCPMap.h
	pushd $@; $(MAKE); popd

yast-ruby-bindings:
	pushd $@; cmake -DCMAKE_PREFIX_PATH=../ -DCMAKE_INSTALL_PREFIX=$(prefix) CMakeLists.txt && $(MAKE); popd
