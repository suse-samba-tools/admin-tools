from yast import Declare, ycpbuiltins
import os.path
from shutil import which

distro = None

@Declare('string')
def Distro():
    global distro
    if distro:
        return distro
    distro = 'unknown'
    if os.path.exists('/etc/os-release'):
        os_release = open('/etc/os-release', 'r').read().lower()
        if 'suse' in os_release:
            distro = 'suse'
        elif 'fedora' in os_release or 'redhat' in os_release or 'rhel' in os_release:
            distro = 'redhat'
    elif os.path.exists('/etc/redhat-release'):
        distro = 'redhat'
    elif os.path.exists('/etc/SuSE-release'):
        distro = 'suse'
    elif os.path.exists('/etc/debian_version'):
        distro = 'debian'
    elif os.path.exists('/etc/arch-release'):
        distro = 'arch'
    elif os.path.exists('/etc/gentoo-release'):
        distro = 'gentoo'
    elif os.path.exists('/etc/slackware-version'):
        distro = 'slackware'
    elif os.path.exists('/etc/frugalware-release'):
        distro = 'arch'
    elif os.path.exists('/etc/altlinux-release'):
        distro = 'debian'
    elif os.path.exists('/etc/mandriva-release'):
        distro = 'mandriva'
    elif os.path.exists('/etc/meego-release'):
        distro = 'debian'
    elif os.path.exists('/etc/angstrom-version'):
        distro = 'angstrom'
    elif os.path.exists('/etc/mageia-release'):
        distro = 'mandriva'
    return distro

@Declare('string', 'string')
def ConvertPackageName(package):
    distro = Distro()
    if distro == 'suse':
        return package
    elif distro == 'redhat':
        if package == 'samba-ad-dc':
            return 'samba-dc'
        elif package in ['samba-client', 'samba-winbind', 'samba', 'krb5-server']:
            return package
    elif distro == 'debian':
        if package == 'krb5-server':
            return 'krb5-kdc'
        elif package == 'samba-ad-dc':
            return 'samba'
    ycpbuiltins.y2milestone('Package %s for distribution %s unknown. Please report this to the maintainer of admin-tools' % (package, distro))
    return package

install_cmd = None

@Declare('list')
def InstallCmd():
    global install_cmd
    if install_cmd:
        return install_cmd
    distro = Distro()
    if distro == 'suse' or which('zypper'):
        install_cmd = ['zypper', 'in', '-l', '-y']
    elif distro == 'redhat' or which('yum'):
        install_cmd = ['yum', 'install', '-y']
    elif distro == 'debian' or which('apt-get'):
        install_cmd = ['apt-get', 'install', '-y']
    elif distro == 'arch' or which('pacman'):
        install_cmd = ['pacman', '--noconfirm', '-S']
    elif distro == 'gentoo' or which('emerge'):
        install_cmd = ['emerge', '--ask=n']
    elif distro == 'mandriva' or which('urpmi'):
        install_cmd = ['urpmi', '--auto']
    elif distro == 'angstrom' or which('opkg'):
        install_cmd = ['opkg', 'install']
    else:
        ycpbuiltins.y2error('Install command for distro %s not found' % distro)
    return install_cmd
