import wx

class Dialog(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        # instance variables -------------------------------------------------------------------------------------------
        self.parent = parent

        # PANELS =======================================================================================================
        self.panel_components = wx.Panel(self, wx.ID_ANY)

        # BINDINGS =====================================================================================================

        # LAYOUT =======================================================================================================
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(0, 255, 0))

    def __do_layout(self):
        sizer_panel_main = wx.GridSizer(1, 1, 0, 0)
        sizer_panel_components= wx.GridBagSizer(0, 0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        label_1 = wx.StaticText(self.panel_components, wx.ID_ANY, "DIALOG")
        label_1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_panel_components.Add(label_1, (row, 0), (1, 3), 0, 0)

        row += 1
        # ...

        # add to main panel --------------------------------------------------------------------------------------------
        sizer_panel_main.Add(self.panel_components, 0, wx.EXPAND | wx.RIGHT, 0)
        # sizer_panel_main.AddGrowableRow(0)
        # sizer_panel_main.AddGrowableCol(1)

        self.SetSizer(sizer_panel_main)
        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1028, 278))
        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = Dialog(self.panel_main)

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

