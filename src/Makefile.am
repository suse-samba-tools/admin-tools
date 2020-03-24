AM_MAKEFLAGS = DEVTOOLSBINDIR=$(abs_top_srcdir)/src/yast-core/base/tools/devtools

SUBDIRS = yast-core libyui libyui-ncurses yast-ycp-ui-bindings yast-python-bindings clients

all: yast-ruby-bindings

.PHONY: yast-ruby-bindings

yast-ruby-bindings: yast-ycp-ui-bindings
	ln -fs $(srcdir)/yast-core/scr/src $(srcdir)/scr
	pushd $@; cmake -DCMAKE_CXX_FLAGS="-I$(abs_top_srcdir)/src/yast-core/liby2util-r/src/include -I$(abs_top_srcdir)/src/yast-core/libycp/src/include -I$(abs_top_srcdir)/src/yast-core/libscr/src/include -I$(abs_top_srcdir)/src" -DCMAKE_PREFIX_PATH=$(abs_top_srcdir)/src/ -DCMAKE_INSTALL_PREFIX=$(prefix) CMakeLists.txt && $(MAKE) --trace && popd

clean-local:
	pushd yast-ruby-bindings; $(MAKE) clean && popd

install-exec-hook:
	pushd yast-ruby-bindings; $(MAKE) install && popd
	pushd yast-rake; rake install && popd
	pushd yast-yast2; rake install && popd
	pushd yast2-adcommon-python; ./setup.py install --prefix=$(prefix) && popd
	pushd yast2-adsi; rake install && popd
	pushd yast2-aduc; rake install && popd
	pushd yast2-dns-manager; rake install && popd
	pushd yast2-gpmc; rake install && popd

CLEANFILES = ycp-ui wfm scr yui YastConfig.cmake
