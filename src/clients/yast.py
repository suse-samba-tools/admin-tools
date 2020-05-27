import yui
from abc import ABC, abstractmethod

class ycpbuiltins(object):
    @staticmethod
    def y2error(msg):
        yui.YUILog_error(msg)

class UI(object):
    f = yui.YUI.widgetFactory()
    ds = []

    @staticmethod
    def OpenDialog(*args):
        opts = []
        widget = None
        for arg in args:
            if type(arg) == Opt:
                opts.extend(arg.opts())
            elif issubclass(type(arg), Widget):
                widget = arg
        if 'mainDialog' in opts:
            UI.ds.append(UI.f.createMainDialog())
        else:
            UI.ds.append(UI.f.createPopupDialog())
        if widget:
            widget.__create__(UI.ds[-1])

    @staticmethod
    def WaitForEvent():
        event = UI.ds[-1].waitForEvent()
        ret = {}
        if event.widget():
            ret['ID'] = event.widget().id().toString()
        if event.eventType() == yui.YEvent.WidgetEvent:
            event.__class__ = yui.YWidgetEvent
            ret['EventReason'] = event.toString(event.reason())
        return ret

    @staticmethod
    def SetApplicationTitle(title):
        pass

class Id(object):
    def __init__(self, label):
        self.id = label

    def __str__(self):
        return self.id

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
        if self.id:
            v.setId(yui.YStringWidgetID(str(self.id)))
        for w in self.widgets:
            w.__create__(v)

class Table(Widget):
    def __init__(self, *args):
        super(Table, self).__init__(*args)

    def __create__(self, parent):
        t = UI.f.createTable(parent, self.args[0])
        if self.id:
            t.setId(yui.YStringWidgetID(str(self.id)))
        if len(self.args) != 2 or type(self.args[-1]) != list:
            raise ValueError(str(self.args))
        for i in self.args[-1]:
            t.addItem(i)

class VSpacing(Widget):
    def __init__(self, *args):
        super(VSpacing, self).__init__(*args)

    def __create__(self, parent):
        v = UI.f.createVSpacing(parent)
        if self.id:
            v.setId(yui.YStringWidgetID(str(self.id)))

class Right(Widget):
    def __init__(self, *args):
        super(Right, self).__init__(*args)

    def __create__(self, parent):
        r = UI.f.createRight(parent)
        if self.id:
            r.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(r)

class HBox(Widget):
    def __init__(self, *args):
        super(HBox, self).__init__(*args)

    def __create__(self, parent):
        h = UI.f.createHBox(parent)
        if self.id:
            h.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(h)

class PushButton(Widget):
    def __init__(self, *args):
        super(PushButton, self).__init__(*args)

    def __create__(self, parent):
        if len(self.args) != 1 or type(self.args[-1]) != str:
            raise ValueError(str(self.args))
        b = UI.f.createPushButton(parent, self.args[-1])
        if self.id:
            b.setId(yui.YStringWidgetID(str(self.id)))
