AM_MAKEFLAGS = DEVTOOLSBINDIR=$(abs_top_srcdir)/src/yast-core/base/tools/devtools

SUBDIRS = yast-core libyui libyui-ncurses yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings clients

DESTDIR ?= /
install-exec-hook:
	pushd yast-yast2; rake install && popd
	pushd yast2-adcommon-python; $(PYTHON) ./setup.py install --no-compile --prefix=$(prefix) --single-version-externally-managed --root=$(DESTDIR) --verbose && popd
	pushd yast2-adsi; rake install && popd
	pushd yast2-aduc; rake install && popd
	pushd yast2-dns-manager; rake install && popd
	pushd yast2-gpmc; rake install && popd

CLEANFILES = ycp-ui wfm scr yui YastConfig.cmake
