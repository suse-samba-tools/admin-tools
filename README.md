# admin-tools

## Installing build dependencies

Installing the admin-tools modules requires the yast-rake ruby gem.
```shell
sudo gem install yast-rake
```

### Debian/Ubuntu
```shell
sudo apt-get install git make automake autoconf autoconf-archive gcc g++ python3-dev swig cmake pkg-config libtool gettext libboost-dev libboost-test-dev bison expect dejagnu doxygen docbook-xsl libncurses6 libncurses-dev libfl-dev libxcrypt1 libxcrypt-dev libjemalloc2 libjemalloc-dev ruby ruby-dev
```

Debian 10 users can install libxcrypt from [my repository here](https://download.opensuse.org/repositories/home:/dmulder:/buster/Debian_10/).

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
python3-samba

## Ruby gems created
packaging yast-rake fast_gettext
