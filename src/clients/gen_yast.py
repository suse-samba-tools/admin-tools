#!/usr/bin/python3

create_id = 'if self.id:\n            w.setId(yui.YStringWidgetID(str(self.id)))\n'
create_widgets = 'for s in self.widgets:\n            s.__create__(w)\n'

create_args = {'Alignment': '', 'InputField': '', 'ProgressBar': '', 'Bottom': '', 'IntField': '', 'PushButton': 'if len(self.args) != 1 or type(self.args[-1]) != str:\n            raise ValueError(str(self.args))\n        w = UI.f.createPushButton(parent, self.args[-1])\n        %s' % create_id, 'BusyIndicator': '', 'ItemSelector': '', 'RadioButton': '', 'ButtonBox': '', 'Label': '', 'RadioButtonGroup': '', 'CheckBox': '', 'LayoutBox': '', 'ReplacePoint': '', 'CheckBoxFrame': '', 'Left': '', 'RichText': '', 'ComboBox': '', 'LogView': '', 'Right': '', 'CustomStatusItemSelector': '', 'MainDialog': '', 'SelectionBox': '', 'Dialog': '', 'MarginBox': '', 'SingleItemSelector': '', 'Empty': '', 'MenuButton': '', 'Spacing': 'raise NotImplementedError(\'Spacing\')', 'Frame': '', 'MinHeight': '', 'Squash': '', 'HBox': '', 'MinSize': '', 'Table': 'w = UI.f.createTable(parent, self.args[0])\n        %s        if len(self.args) != 2 or type(self.args[-1]) != list:\n            raise ValueError(str(self.args))\n        for i in self.args[-1]:\n            t.addItem(i)\n' % create_id, 'HCenter': '', 'MinWidth': '', 'Top': '', 'Heading': '', 'MultiItemSelector': '', 'Tree': '', 'HSpacing': 'if len(self.args) != 1:\n            raise ValueError(str(self.args))\n        w = UI.f.createHSpacing(parent, self.args[-1])\n        %s        %s' % (create_id, create_widgets), 'MultiLineEdit': '', 'VBox': '', 'HSquash': '', 'MultiSelectionBox': '', 'VCenter': '', 'HStretch': '', 'OutputField': '', 'VSpacing': 'if len(self.args) != 1:\n            raise ValueError(str(self.args))\n        w = UI.f.createVSpacing(parent, self.args[-1])\n        %s        %s' % (create_id, create_widgets), 'HVCenter': '', 'PackageSelector': '', 'VSquash': '', 'HVSquash': '', 'PasswordField': '', 'VStretch': '', 'IconButton': '', 'PkgSpecial': '', 'Image': '', 'PopupDialog': ''}

typical_create = 'if len(self.args) != 0:\n            raise NotImplementedError(\'%s: \'+str(self.args))\n        w = UI.f.create%s(parent)\n        %s        %s'

for a in create_args.keys():
    if create_args[a]:
        create = create_args[a]
    else:
        create = typical_create % (a, a, create_id, create_widgets)
    print('class %s(Widget):\n    def __init__(self, *args):\n        super(%s, self).__init__(*args)\n\n    def __create__(self, parent):\n        %s' % (a, a, create))
