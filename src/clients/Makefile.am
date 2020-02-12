
y2basedir = $(prefix)/lib/YaST2/bin

admin-tools: admin-tools.in
	sed -e 's;[@]Y2BASEDIR[@];$(y2basedir);g' < $^ > $@

yast_clientdir = $(datadir)/YaST2/clients
yast_client_DATA = admin-tools.py

bin_SCRIPTS = admin-tools

CLEANFILES = admin-tools
