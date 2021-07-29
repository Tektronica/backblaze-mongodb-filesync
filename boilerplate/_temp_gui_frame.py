import wx
from _temp_gui_panel import MyPanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1028, 278))

        # PANELS =======================================================================================================
        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = MyPanel(self.panel_main)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Dialog")

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_components = wx.GridBagSizer(0, 0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        sizer_components.Add(self.panel_dialog, (row, 1), (1, 1), wx.ALL | wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_components)

        row += 1
        
        sizer_main.Add(self.panel_main, 1, wx.ALL | wx.EXPAND, 10)

        sizer_components.AddGrowableRow(0)
        sizer_components.AddGrowableCol(1)

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