import wx
import gettext


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.labelPath = wx.StaticText(self, wx.ID_ANY, name="Path : ")
        self.textCtrlPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_1 = wx.Button(self, wx.ID_ANY, name="Open...")
        self.labelFile = wx.StaticText(self, wx.ID_ANY, name="File List :")
        self.listCtrlFile = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.buttonAccept = wx.Button(self, wx.ID_ANY, name="RUN")
        self.buttonExit = wx.Button(self, wx.ID_ANY, name="EXIT")
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnButtonPath, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAccept, self.buttonAccept)
        self.Bind(wx.EVT_BUTTON, self.OnButtonExit, self.buttonExit)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle(("test"))
        self.textCtrlPath.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer.Add(self.labelPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        pathSizer.Add(self.textCtrlPath, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        pathSizer.Add(self.button_1, 0, 0, 0)
        mainSizer.Add(pathSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)
        mainSizer.Add(self.labelFile, 0, wx.ALL, 6)
        mainSizer.Add(self.listCtrlFile, 7, wx.ALL | wx.EXPAND, 4)
        footerSizer.Add(self.buttonAccept, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        footerSizer.Add(self.buttonExit, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        mainSizer.Add(footerSizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        # end wxGlade

    def OnButtonPath(self, event):  # wxGlade: MyDialog.<event_handler>
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.textCtrlPath.Value = dlg.GetPath()
        dlg.Destroy()

    def OnButtonAccept(self, event):  # wxGlade: MyDialog.<event_handler>
        print("Event handler 'OnButtonAccept' not implemented!")
        event.Skip()

    def OnButtonExit(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Destroy()

# end of class MyDialog
if __name__ == "__main__":
    gettext.install("test") # replace with the appropriate catalog name

    test = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainDialog = MyDialog(None, wx.ID_ANY, "")
    test.SetTopWindow(mainDialog)
    mainDialog.Show()
    test.MainLoop()