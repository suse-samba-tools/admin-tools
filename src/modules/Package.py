from yast import Declare, ycpbuiltins, import_module
import_module('Platform')
from yast import Platform
from subprocess import Popen, PIPE

@Declare('boolean', 'list')
def InstallAll(packages):
    ycpbuiltins.y2milestone('Packages %s were requested to be installed' % ', '.join(packages))
    install_cmd = Platform.InstallCmd()
    if install_cmd:
        for package in packages:
            package = Platform.ConvertPackageName(package)
            cmd = list(install_cmd)
            cmd.append(package)
            ycpbuiltins.y2error(' '.join(cmd))
            ret = Popen(cmd, stdout=PIPE, stderr=PIPE).wait()
            if ret != 0:
                ycpbuiltins.y2error('Package %s failed to install!' % package)
    return True
