from yast import Declare, ycpbuiltins

@Declare('boolean')
def Read():
    return True

@Declare('boolean')
def WriteOnly():
    return True

@Declare('boolean')
def ActivateConfiguration():
    return True
