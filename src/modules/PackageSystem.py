from yast import Declare, ycpbuiltins, import_module
import_module('Package')
from yast import Package

@Declare('boolean', 'string')
def Installed(package):
    ycpbuiltins.y2milestone('Package %s was requested to be installed' % package)
    return True

@Declare('boolean', 'list')
def CheckAndInstallPackagesInteractive(packages):
    ycpbuiltins.y2milestone('Packages %s were requested to be installed' % ', '.join(packages))
    for package in packages:
        if not Installed(package):
            Package.InstallAll([package])
    return True
