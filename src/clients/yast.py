import yui
from abc import ABC, abstractmethod

class UI(object):
    f = yui.YUI.widgetFactory()
    ds = []

    @staticmethod
    def OpenDialog(*args):
        self.optis = []
        self.widget = None
        for arg in args:
            if type(arg) == Opt:
                self.opts.extend(arg.opts())
            elif issubclass(type(arg), Widget):
                self.widget = arg
        UI.ds.append(UI.f.createMainDialog())

    @staticmethod
    def WaitForEvent():
        return UI.ds[-1].waitForEvent()

    @staticmethod
    def SetApplicationTitle(title):
        pass

class Id(object):
    def __init__(self, label):
        self.id = label

class Opt(object):
    def __init__(self, *args):
        self._opts = args

    def opts(self):
        return self._opts

def Header(*args):
    h = yui.YTableHeader()
    for arg in args:
        h.addColumn(arg)
    return h

def Item(*args):
    item_id = None
    for arg in args:
        if type(arg) == Id:
            item_id = arg
        else:
            label = arg
    # TODO: How to set the id?
    return yui.YTableItem(label)

class Widget(ABC):
    def __init__(self, *args):
        self.args = []
        self.id = None
        self.opts = []
        self.widgets = []
        for arg in args:
            if type(arg) == Id:
                self.id = arg
            elif type(arg) == Opt:
                self.opts.extend(arg.opts())
            elif issubclass(type(arg), Widget):
                self.widgets.append(arg)
            else:
                self.args.append(arg)

    @abstractmethod
    def __create__(self, parent):
        pass

class VBox(Widget):
    def __init__(self, *args):
        super(VBox, self).__init__(*args)

    def __create__(self, parent):
        v = UI.f.createVBox(parent)
        for w in self.widgets:
            w.__create__(v)

class Table(Widget):
    def __init__(self, *args):
        super(Table, self).__init__(*args)

    def __create__(self, parent):
        t = UI.f.createTable(parent)
        if len(self.args) != 1 or type(self.args[-1]) != list:
            raise ValueError(str(self.args))
        for i in self.args[-1]:
            i.__create__(t)
