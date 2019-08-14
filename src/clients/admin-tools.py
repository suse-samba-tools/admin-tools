#!/usr/bin/python3
from yast import import_module
import_module('UI')
from yast import *
from subprocess import Popen
import os

def choose_module():
    header = Header('Name')
    items = [Item(Id('aduc'), 'Active Directory Users and Computers'),
             Item(Id('adsi'), 'ADSI Edit'),
             Item(Id('dns-manager'), 'DNS'),
             Item(Id('gpmc'), 'Group Policy Management Console'),
             Item(Id('samba-provision'), 'Provision an Active Directory Domain Controller'),
    ]
    UI.OpenDialog(Opt('mainDialog'), Table(Id('tools'), Opt('notify'), header, items))
    UI.SetApplicationTitle('Administrative Tools')

    UI.WaitForEvent()
    module = UI.QueryWidget('tools', 'Value')
    UI.CloseDialog()

    return module

def warn_message(title, msg):
    UI.SetApplicationTitle(title)
    UI.OpenDialog(Opt('warncolor'), HBox(HSpacing(1), VBox(
        VSpacing(.3),
        Label(msg),
        Right(HBox(
            PushButton('OK'),
        )),
        VSpacing(.3),
    ), HSpacing(1)))
    UI.UserInput()
    UI.CloseDialog()

def run(module):
    if module in ['samba-provision']:
        if os.geteuid() != 0:
            warn_message('Authenticate', 'To continue, you must be authenticated as a privileged user.')
            return
    Popen(['y2base', module, 'ncurses']).wait()

if __name__ == "__main__":
    module = choose_module()
    run(module)
