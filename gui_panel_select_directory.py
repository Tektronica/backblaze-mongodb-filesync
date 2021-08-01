import wx
import threading
import time


class Directory(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        # instance variables -------------------------------------------------------------------------------------------
        self.parent = parent
        self.frame = frame
        self.path = '/'
        self.active_thread = None

        # PANELS =======================================================================================================
        self.panel_components = wx.Panel(self, wx.ID_ANY)

        # COMPONENTS ===================================================================================================
        self.text_directory = wx.TextCtrl(self, wx.ID_ANY, "")  # style=wx.TE_READONLY
        self.Bind(wx.EVT_TEXT, self.text_event, self.text_directory)

        self.btn_open_dialog = wx.Button(self, wx.ID_ANY, "Open File Dialog")
        self.Bind(wx.EVT_BUTTON, self.dirDialog, self.btn_open_dialog)

        # LAYOUT =======================================================================================================
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(252, 211, 77))
        self.text_directory.SetMinSize((400, 23))

    def __do_layout(self):
        sizer_panel_components = wx.GridBagSizer(0, 0)


        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        label_1 = wx.StaticText(self, wx.ID_ANY, "DIRECTORY")
        label_1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_panel_components.Add(label_1, (row, 0), (1, 3), 0, 0)

        row += 1
        sizer_panel_components.Add(self.btn_open_dialog, (row, 0), (1, 1), wx.ALL, 5)
        sizer_panel_components.Add(self.text_directory, (row, 1), (1, 2), wx.ALL | wx.EXPAND, 5)

        row += 1
        # ...

        sizer_panel_components.AddGrowableCol(1)

        self.SetSizer(sizer_panel_components)
        self.Layout()

    def dirDialog(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            path_to_folder = dlg.GetPath()
            print(f"You chose {path_to_folder}")
            self.text_directory.SetValue(path_to_folder)
            self.path = path_to_folder
        dlg.Destroy()
        

    def text_event(self, evt):
        if not self.active_thread:
            self.active_thread = EventThread(self)
        else:
            self.active_thread.newSig()

    def done(self):
        self.active_thread = None

        if self.frame is not None:
            self.frame.panel_dialog.first_update(self.path)


class EventThread(threading.Thread):
    def __init__(self, panel):
        threading.Thread.__init__(self)
        self.count = 0
        self.panel = panel
        self.start()

    # hangs event until after time delay. Allows user a brief typing pause allowance
    def run(self):
        while self.count < 1.0:
            time.sleep(0.1)
            self.count += 0.1

        self.panel.done()

    def newSig(self):
        print("thread notified of new EVT_TEXT. Resetting count.")
        self.count = 0


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1028, 278))
        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = Directory(self.panel_main, None)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Dialog")

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_components = wx.BoxSizer(wx.VERTICAL)

        sizer_components.Add(self.panel_dialog, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_components)

        sizer_main.Add(self.panel_main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
