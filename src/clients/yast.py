import yui, yui_ext
from abc import ABC, abstractmethod

def import_module(name):
    pass

class ycpbuiltins(object):
    @staticmethod
    def y2error(msg):
        yui.YUILog_error(msg)

class Code(object):
    pass

class Symbol(object):
    def __init__(self, label):
        self.symbol = label

    def __str__(self):
        return self.symbol

class Sequencer:
    def __init__(self, *cli_args):
        self.cli_args = cli_args

    def run(self, funcs):
        Wizard.CreateDialog()

        for func in funcs:
            ret = func(*self.cli_args)
            if type(ret) is tuple:
                data, ret = ret
                self.cli_args = (data,) + self.cli_args
            if str(ret) == 'next':
                continue
            elif str(ret) == 'abort':
                break

        UI.CloseDialog()

class Wizard(object):
    @staticmethod
    def GenericDialog(button_box):
        return VBox(
            Id('WizardDialog'),
            ReplacePoint(Id('topmenu'), Empty()),
            HBox(
                HSpacing(1),
                VBox(
                    VSpacing(0.2),
                    HBox(
                        Heading(Id('title'), Opt('hstretch'), "Initializing ..."),
                        HStretch(),
                        ReplacePoint(Id('relnotes_rp'), Empty())
                    ),
                    VWeight(
                        1,
                        HVCenter(Opt('hvstretch'), ReplacePoint(Id('contents'), Empty()))
                    )
                ),
                HSpacing(1)
            ),
            ReplacePoint(Id('rep_button_box'), button_box),
            VSpacing(0.2)
        )

    @staticmethod
    def BackAbortNextButtonBox():
        return HBox(
            HWeight(1, ReplacePoint(Id('rep_help'),
                PushButton(Id('help'), Opt('key_F1', 'helpButton'), 'Help')
            )),
            HStretch(),
            HWeight(1, ReplacePoint(Id('rep_back'),
                PushButton(Id('back'), Opt('key_F8'), 'Back')
            )),
            HStretch(),
            ReplacePoint(Id('rep_abort'),
                PushButton(Id('abort'), Opt('key_F9'), 'Abort')
            ),
            HStretch(),
            HWeight(1, ReplacePoint(Id('rep_next'),
                PushButton(Id('next'), Opt('key_F10', 'default'), 'Next')
            )),
        )

    @staticmethod
    def CreateDialog():
        content = Wizard.GenericDialog(Wizard.BackAbortNextButtonBox())
        UI.OpenDialog(content, Opt('wizardDialog'))
        UI.SetFocus('next')

    @staticmethod
    def SetContentsButtons(title, contents, help_txt, back_txt, next_txt):
        UI.SetApplicationTitle(title)
        UI.ChangeWidget('title', 'Value', title)
        UI.ReplaceWidget('contents', contents)
        UI.ReplaceWidget('rep_back', PushButton(Id('back'), Opt('key_F8'), back_txt))
        UI.ReplaceWidget('rep_next', PushButton(Id('next'), Opt('key_F10', 'default'), next_txt))

    @staticmethod
    def DisableBackButton():
        pass

    @staticmethod
    def DisableNextButton():
        pass

    @staticmethod
    def EnableNextButton():
        pass

    @staticmethod
    def DisableAbortButton():
        pass

    @staticmethod
    def SetTitleIcon(icon_name):
        UI.a.setApplicationIcon(icon_name)

class UI(object):
    f = yui.YUI.widgetFactory()
    o = yui.YUI.optionalWidgetFactory()
    a = yui.YUI_application()
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
            reason = yui_ext.YWidgetEvent_reason(event)
            if reason == 0: # UnknownReason
                ret['EventReason'] = 'UnknownReason'
            elif reason == 1: # Activated
                ret['EventReason'] = 'Activated'
            elif reason == 2: # SelectionChanged
                ret['EventReason'] = 'SelectionChanged'
            elif reason == 3: # ValueChanged
                ret['EventReason'] = 'ValueChanged'
            elif reason == 4: # ContextMenuActivated
                ret['EventReason'] = 'ContextMenuActivated'
        return ret

    @staticmethod
    def SetApplicationTitle(title):
        UI.a.setApplicationTitle(title)

    @staticmethod
    def HasSpecialWidget(name):
        if name == 'Graph':
            return UI.o.hasGraph()
        elif name == 'MultiProgressMeter':
            return UI.o.hasMultiProgressMeter()
        elif name == 'PartitionSplitter':
            return UI.o.hasPartitionSplitter()
        elif name == 'PatternSelector':
            return UI.o.hasPatternSelector()
        elif name == 'SimplePatchSelector':
            return UI.o.hasSimplePatchSelector()
        elif name == 'BarGraph':
            return UI.o.hasBarGraph()
        elif name == 'Slider':
            return UI.o.hasSlider()
        elif name == 'ContextMenu':
            return UI.o.hasContextMenu()
        elif name == 'TimeField':
            return UI.o.hasTimeField()
        elif name == 'DateField':
            return UI.o.hasDateField()
        elif name == 'TimezoneSelector':
            return UI.o.hasTimezoneSelector()
        elif name == 'DownloadProgress':
            return UI.o.hasDownloadProgress()
        elif name == 'Wizard':
            return UI.o.hasWizard()
        elif name == 'DumbTab':
            return UI.o.hasDumbTab()
        elif name == 'DummySpecialWidget':
            return UI.o.hasDummySpecialWidget()

    @staticmethod
    def SetFocus(wid):
        # TODO: Discover how to set the focus
        pass # yui.YUIBuiltin_SetFocus

    @staticmethod
    def WizardCommand(*args):
        # TODO: Define the wizard commands
        pass

    @staticmethod
    def UserInput():
        event = UI.ds[-1].waitForEvent()
        ret = None
        if event.widget():
            ret = event.widget().id().toString()
        return ret

    @staticmethod
    def QueryWidget(wid, wprop):
        try:
            widget = UI.ds[-1].findWidget(yui.YStringWidgetID(wid))
        except YUIWidgetNotFoundException:
            return None
        prop = widget.getProperty(wprop)
        if prop.type() == yui.YStringProperty:
            return prop.stringVal()
        elif prop.type() == yui.YBoolProperty:
            return prop.boolVal()
        elif prop.type() == yui.YIntegerProperty:
            return prop.integerVal()
        else:
            raise NotImplementedError('Property type: %d' % prop.type())

    @staticmethod
    def CloseDialog():
        close_dialog = UI.ds.pop()
        close_dialog.destroy()

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
        self.args = tuple(self.args)

    @abstractmethod
    def __create__(self, parent):
        pass

class HWeight(Widget):
    def __init__(self, *args):
        super(HWeight, self).__init__(*args)

    def __create__(self, parent):
        # TODO: Discover how to build an HWeight, which doesn't exist in libyui
        for s in self.widgets:
            s.__create__(parent)

class VWeight(Widget):
    def __init__(self, *args):
        super(VWeight, self).__init__(*args)

    def __create__(self, parent):
        # TODO: Discover how to build an VWeight, which doesn't exist in libyui
        for s in self.widgets:
            s.__create__(parent)

class Alignment(Widget):
    def __init__(self, *args):
        super(Alignment, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createAlignment(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class InputField(Widget):
    def __init__(self, *args):
        super(InputField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createInputField(parent, self.args[0])
        if len(self.args[0]) > 1:
                w.setValue(self.args[1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)
TextEntry = InputField

class ProgressBar(Widget):
    def __init__(self, *args):
        super(ProgressBar, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createProgressBar(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Bottom(Widget):
    def __init__(self, *args):
        super(Bottom, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createBottom(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class IntField(Widget):
    def __init__(self, *args):
        super(IntField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createIntField(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PushButton(Widget):
    def __init__(self, *args):
        super(PushButton, self).__init__(*args)

    def __create__(self, parent):
        if len(self.args) != 1 or type(self.args[-1]) != str:
            raise ValueError(str(self.args))
        w = UI.f.createPushButton(parent, self.args[-1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))

class BusyIndicator(Widget):
    def __init__(self, *args):
        super(BusyIndicator, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createBusyIndicator(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class ItemSelector(Widget):
    def __init__(self, *args):
        super(ItemSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createItemSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class RadioButton(Widget):
    def __init__(self, *args):
        super(RadioButton, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createRadioButton(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class ButtonBox(Widget):
    def __init__(self, *args):
        super(ButtonBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createButtonBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Label(Widget):
    def __init__(self, *args):
        super(Label, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createLabel(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class RadioButtonGroup(Widget):
    def __init__(self, *args):
        super(RadioButtonGroup, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createRadioButtonGroup(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class CheckBox(Widget):
    def __init__(self, *args):
        super(CheckBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createCheckBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class LayoutBox(Widget):
    def __init__(self, *args):
        super(LayoutBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createLayoutBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class ReplacePoint(Widget):
    def __init__(self, *args):
        super(ReplacePoint, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createReplacePoint(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class CheckBoxFrame(Widget):
    def __init__(self, *args):
        super(CheckBoxFrame, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createCheckBoxFrame(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Left(Widget):
    def __init__(self, *args):
        super(Left, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createLeft(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class RichText(Widget):
    def __init__(self, *args):
        super(RichText, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createRichText(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class ComboBox(Widget):
    def __init__(self, *args):
        super(ComboBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createComboBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class LogView(Widget):
    def __init__(self, *args):
        super(LogView, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createLogView(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Right(Widget):
    def __init__(self, *args):
        super(Right, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createRight(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class CustomStatusItemSelector(Widget):
    def __init__(self, *args):
        super(CustomStatusItemSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createCustomStatusItemSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MainDialog(Widget):
    def __init__(self, *args):
        super(MainDialog, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMainDialog(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class SelectionBox(Widget):
    def __init__(self, *args):
        super(SelectionBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createSelectionBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Dialog(Widget):
    def __init__(self, *args):
        super(Dialog, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createDialog(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MarginBox(Widget):
    def __init__(self, *args):
        super(MarginBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMarginBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class SingleItemSelector(Widget):
    def __init__(self, *args):
        super(SingleItemSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createSingleItemSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Empty(Widget):
    def __init__(self, *args):
        super(Empty, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createEmpty(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MenuButton(Widget):
    def __init__(self, *args):
        super(MenuButton, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMenuButton(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Spacing(Widget):
    def __init__(self, *args):
        super(Spacing, self).__init__(*args)

    def __create__(self, parent):
        raise NotImplementedError('Spacing')
class Frame(Widget):
    def __init__(self, *args):
        super(Frame, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createFrame(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MinHeight(Widget):
    def __init__(self, *args):
        super(MinHeight, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMinHeight(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Squash(Widget):
    def __init__(self, *args):
        super(Squash, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createSquash(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HBox(Widget):
    def __init__(self, *args):
        super(HBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MinSize(Widget):
    def __init__(self, *args):
        super(MinSize, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMinSize(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Table(Widget):
    def __init__(self, *args):
        super(Table, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createTable(parent, self.args[0])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        if len(self.args) != 2 or type(self.args[-1]) != list:
            raise ValueError(str(self.args))
        for i in self.args[-1]:
            w.addItem(i)

class HCenter(Widget):
    def __init__(self, *args):
        super(HCenter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHCenter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MinWidth(Widget):
    def __init__(self, *args):
        super(MinWidth, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMinWidth(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Top(Widget):
    def __init__(self, *args):
        super(Top, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createTop(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Heading(Widget):
    def __init__(self, *args):
        super(Heading, self).__init__(*args)

    def __create__(self, parent):
        if len(self.args) != 1:
            raise ValueError(str(self.args))
        w = UI.f.createHeading(parent, self.args[-1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MultiItemSelector(Widget):
    def __init__(self, *args):
        super(MultiItemSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMultiItemSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Tree(Widget):
    def __init__(self, *args):
        super(Tree, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createTree(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HSpacing(Widget):
    def __init__(self, *args):
        super(HSpacing, self).__init__(*args)

    def __create__(self, parent):
        if len(self.args) != 1:
            raise ValueError(str(self.args))
        w = UI.f.createHSpacing(parent, self.args[-1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MultiLineEdit(Widget):
    def __init__(self, *args):
        super(MultiLineEdit, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMultiLineEdit(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class VBox(Widget):
    def __init__(self, *args):
        super(VBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createVBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HSquash(Widget):
    def __init__(self, *args):
        super(HSquash, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHSquash(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MultiSelectionBox(Widget):
    def __init__(self, *args):
        super(MultiSelectionBox, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createMultiSelectionBox(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class VCenter(Widget):
    def __init__(self, *args):
        super(VCenter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createVCenter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HStretch(Widget):
    def __init__(self, *args):
        super(HStretch, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHStretch(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class OutputField(Widget):
    def __init__(self, *args):
        super(OutputField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createOutputField(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class VSpacing(Widget):
    def __init__(self, *args):
        super(VSpacing, self).__init__(*args)

    def __create__(self, parent):
        if len(self.args) != 1:
            raise ValueError(str(self.args))
        w = UI.f.createVSpacing(parent, self.args[-1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HVCenter(Widget):
    def __init__(self, *args):
        super(HVCenter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHVCenter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PackageSelector(Widget):
    def __init__(self, *args):
        super(PackageSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createPackageSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class VSquash(Widget):
    def __init__(self, *args):
        super(VSquash, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createVSquash(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HVSquash(Widget):
    def __init__(self, *args):
        super(HVSquash, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createHVSquash(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PasswordField(Widget):
    def __init__(self, *args):
        super(PasswordField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createPasswordField(parent, self.args[0])
        if len(self.args[0]) > 1:
                w.setValue(self.args[1])
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)
Password = PasswordField

class VStretch(Widget):
    def __init__(self, *args):
        super(VStretch, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createVStretch(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class IconButton(Widget):
    def __init__(self, *args):
        super(IconButton, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createIconButton(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PkgSpecial(Widget):
    def __init__(self, *args):
        super(PkgSpecial, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createPkgSpecial(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Image(Widget):
    def __init__(self, *args):
        super(Image, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createImage(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PopupDialog(Widget):
    def __init__(self, *args):
        super(PopupDialog, self).__init__(*args)

    def __create__(self, parent):
        w = UI.f.createPopupDialog(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class BarGraph(Widget):
    def __init__(self, *args):
        super(BarGraph, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createBarGraph(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Slider(Widget):
    def __init__(self, *args):
        super(Slider, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createSlider(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class DateField(Widget):
    def __init__(self, *args):
        super(DateField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createDateField(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class TimeField(Widget):
    def __init__(self, *args):
        super(TimeField, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createTimeField(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class DownloadProgress(Widget):
    def __init__(self, *args):
        super(DownloadProgress, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createDownloadProgress(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class TimezoneSelector(Widget):
    def __init__(self, *args):
        super(TimezoneSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createTimezoneSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class DumbTab(Widget):
    def __init__(self, *args):
        super(DumbTab, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createDumbTab(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class VMultiProgressMeter(Widget):
    def __init__(self, *args):
        super(VMultiProgressMeter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createVMultiProgressMeter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class DummySpecialWidget(Widget):
    def __init__(self, *args):
        super(DummySpecialWidget, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createDummySpecialWidget(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class Graph(Widget):
    def __init__(self, *args):
        super(Graph, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createGraph(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class HMultiProgressMeter(Widget):
    def __init__(self, *args):
        super(HMultiProgressMeter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createHMultiProgressMeter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class MultiProgressMeter(Widget):
    def __init__(self, *args):
        super(MultiProgressMeter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createMultiProgressMeter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PartitionSplitter(Widget):
    def __init__(self, *args):
        super(PartitionSplitter, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createPartitionSplitter(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class PatternSelector(Widget):
    def __init__(self, *args):
        super(PatternSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createPatternSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)

class SimplePatchSelector(Widget):
    def __init__(self, *args):
        super(SimplePatchSelector, self).__init__(*args)

    def __create__(self, parent):
        w = UI.o.createSimplePatchSelector(parent, *self.args)
        if self.id:
            w.setId(yui.YStringWidgetID(str(self.id)))
        for s in self.widgets:
            s.__create__(w)
