# admin-tools

Administrator Tools is built using numerous packages, but the important repositories are [admin-tools](https://github.com/suse-samba-tools/admin-tools), [yast2-aduc](https://github.com/yast/yast2-aduc), [yast2-adsi](https://github.com/yast/yast2-adsi), [yast2-dns-manager](https://github.com/yast/yast2-dns-manager), and [yast2-gpmc](https://github.com/yast/yast2-gpmc). These packages are bundled into an [appimage and published on the AppImageHub](https://appimage.github.io/admin-tools/). Administrator Tools uses YaST as it's backend, more specifically it primarily uses the [YaST python bindings](https://github.com/yast/yast-python-bindings).

To work on one of the individual tools, fork the repository on github, then submit a pull request to the project. To work on the main menu or automated testing, fork the admin-tools project.

[Take a look at current tasks](https://dev.azure.com/suse-samba-tools/admin-tools/_boards) if you want to help out.

## Installing build dependencies

Installing the admin-tools modules requires the yast-rake ruby gem.
```shell
sudo gem install yast-rake
```

### Debian/Ubuntu
```shell
sudo apt-get install git make automake autoconf autoconf-archive gcc g++ python3-dev swig cmake pkg-config libtool gettext libboost-dev libboost-test-dev bison expect dejagnu doxygen docbook-xsl libncurses6 libncurses-dev libfl-dev libjemalloc2 libjemalloc-dev ruby ruby-dev
```

Packages libxcrypt1 libxcrypt-dev are also required to build admin-tools, but are not distributed in Debian distros. I've built these packages for your use and have them hosted in [my repository here](https://download.opensuse.org/repositories/home:/dmulder:/buster/).

### openSUSE
```shell
sudo zypper install make automake autoconf gcc gcc-c++ dejagnu flex libboost_headers1_66_0-devel jemalloc jemalloc-devel autoconf-archive python3-devel swig docbook-xsl-stylesheets libboost_test1_66_0-devel ncurses-devel ruby-devel
```

### Redhat
```shell
sudo yum install make gcc autoconf automake gcc-c++ dejagnu flex autoconf-archive python3-devel swig  ncurses-devel ruby-devel cmake libtool boost-devel boost-test doxygen bison perl-devel perl-Pod-Html jemalloc jemalloc-devel rake
```

## Build instructions

```shell
git clone https://github.com/suse-samba-tools/admin-tools.git
cd admin-tools
git submodule init
git submodule update
./autogen.sh && ./configure
make && sudo make install
```

## Run-time dependencies

Adminstrative Tools requires that Samba be installed. Follow the [instructions found in the Samba wiki](https://wiki.samba.org/index.php/Distribution-specific_Package_Installation) to install it for your distribution.
