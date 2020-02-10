SUBDIRS = yast-core libyui libyui-ncurses

all: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

.PHONY: yast-ycp-ui-bindings yast-python-bindings yast-ruby-bindings

yast-ycp-ui-bindings:
	pushd $@; $(MAKE) DEVTOOLSBINDIR=../../yast-core/base/tools/devtools; popd

yast-python-bindings:
	pushd $@; $(MAKE); popd

yast-ruby-bindings:
	pushd $@; $(MAKE); popd
