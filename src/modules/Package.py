from yast import Declare, ycpbuiltins
import os.path

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
        elif 'fedora' in os_release or 'redhat' in os_release:
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
        distro = 'frugalware'
    elif os.path.exists('/etc/altlinux-release'):
        distro = 'altlinux'
    elif os.path.exists('/etc/mandriva-release'):
        distro = 'mandriva'
    elif os.path.exists('/etc/meego-release'):
        distro = 'meego'
    elif os.path.exists('/etc/angstrom-version'):
        distro = 'angstrom'
    elif os.path.exists('/etc/mageia-release'):
        distro = 'mageia'
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
    ycpbuiltins.y2milestone('Package %s for distribution %s unknown. Please report this to the maintainer of admin-tools' % (package, distro))
    return package

@Declare('boolean', 'list')
def InstallAll(packages):
    ycpbuiltins.y2milestone('Packages %s were requested to be installed' % ', '.join(packages))
    for package in packages:
        package = ConvertPackageName(package)
    return True
