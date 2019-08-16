#!/usr/bin/python3
from yast import import_module
import_module('UI')
from yast import *
from subprocess import Popen
import os

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

def update():
    UI.SetApplicationTitle('Checking for updates...')
    UI.OpenDialog(Label('Checking for updates, please wait...'))
    ret = os.system('appimageupdatetool -j $APPIMAGE')
    UI.CloseDialog()
    if ret == 1:
        UI.SetApplicationTitle('Updating...')
        UI.OpenDialog(Label('Updating, please wait...'))
        ret = os.system('appimageupdatetool -O $APPIMAGE')
        UI.CloseDialog()
        if ret == 0:
            warn_message('Update', 'Successfully updated!')
        else:
            warn_message('Update', 'Update failed!')
    elif ret == 0:
        warn_message('Update', 'No updates are available.')
    else:
        warn_message('Update', 'Failed to check for updates!')
    UI.SetApplicationTitle('Administrative Tools')

def choose_module():
    module = None
    header = Header('Name')
    items = [Item(Id('aduc'), 'Active Directory Users and Computers'),
             Item(Id('adsi'), 'ADSI Edit'),
             Item(Id('dns-manager'), 'DNS'),
             Item(Id('gpmc'), 'Group Policy Management'),
    ]
    dialog = VBox(
        Table(Id('tools'), Opt('notify'), header, items),
        VSpacing(.3),
        Right(HBox(
            PushButton(Id('update'), 'Update'),
            PushButton(Id('close'), 'Close'),
        ))
    )
    UI.OpenDialog(Opt('mainDialog'), dialog)
    UI.SetApplicationTitle('Administrative Tools')

    while True:
        ret = UI.WaitForEvent()
        ycpbuiltins.y2error(str(ret))
        if ret['ID'] == 'update':
            update()
        elif ret['ID'] == 'close':
            break
        else:
            module = UI.QueryWidget('tools', 'Value')
            break
    UI.CloseDialog()

    return module

def run(module):
    Popen(['y2base', module, 'ncurses']).wait()

if __name__ == "__main__":
    module = choose_module()
    if module:
        run(module)
