
y2basedir = $(prefix)/lib/YaST2/bin

admin-tools: admin-tools.in
	sed -e 's;[@]Y2BASEDIR[@];$(y2basedir);g' < $^ > $@

yast_clientdir = $(datadir)/YaST2/clients
yast_client_DATA = admin-tools.py

bin_SCRIPTS = admin-tools

python_PYTHON = yast.py

yui_ext_wrap.cxx: yui_ext.i yui_ext.h
	$(SWIG) $(AX_SWIG_PYTHON_OPT) -c++ -I$(srcdir)/../libyui/src $(CPPFLAGS) -o $@ $<

SWIG_SOURCES = yui_ext.i

pkgpython_PYTHON = yui_ext.py
pkgpyexec_LTLIBRARIES = _yui_ext.la
_yui_ext_la_SOURCES = yui_ext_wrap.cxx yui_ext.cpp
_yui_ext_la_CPPFLAGS = -I$(srcdir)/../libyui/src $(SWIG_PYTHON_CPPFLAGS) `${PYTHON}-config --cflags`
_yui_ext_la_LDFLAGS = -module
_yui_ext_la_LIBADD = -lyui

CLEANFILES = admin-tools yui_ext_wrap.cxx yui_ext.py
