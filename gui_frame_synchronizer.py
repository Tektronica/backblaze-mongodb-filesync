
import wx
import wx.adv
import wx.html
import warnings

from gui_panel_select_directory import Directory
from gui_panel_dialog import Dialog
from gui_panel_options import Options

APP_VERSION = 'v2.3.1'
APP_ICON = 'images/hornet.ico'


########################################################################################################################
class MyFrame(wx.Frame):
    """"""

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.SetSize((1215, 580))
        # https://stackoverflow.com/a/24704039/3382269
        # Sets minimum window dimensions
        # self.SetSizeHints(1055, 640, -1, -1)

        # MAIN PANEL ===================================================================================================
        self.panel_frame = wx.Panel(self, wx.ID_ANY)
        self.panel_components = wx.Panel(self.panel_frame, wx.ID_ANY)

        self.panel_directory = Directory(self.panel_components, self)
        self.panel_dialog = Dialog(self.panel_components, self)
        self.panel_options = Options(self.panel_components, self)

        # VIEW menu tab ------------------------------------------------------------------------------------------------
        self.frame_menubar = wx.MenuBar()
        menu_tree = wx.Menu()
        self.menu_reset_view = menu_tree.Append(
            wx.ID_ANY, "Reset Window Size", "")
        menu_tree.AppendSeparator()
        # self.menu_brkpts = wxglade_tmp_menu.Append(wx.ID_ANY, "Open Breakpoints", "")
        self.frame_menubar.Append(menu_tree, "View")
        self.SetMenuBar(self.frame_menubar)

        # BINDING EVENTS ===============================================================================================
        self.Bind(wx.EVT_MENU, self.reset_view, self.menu_reset_view)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Freeze()
        self.__set_properties()
        self.__do_layout()
        self.Thaw()

    def __set_properties(self):
        self.SetTitle("Synchronizer")
        self.SetBackgroundColour(wx.Colour(227, 227, 227))

    def __do_layout(self):
        sizer_panel_frame = wx.BoxSizer(wx.VERTICAL)
        sizer_panel_components = wx.GridBagSizer(0, 0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        sizer_panel_components.Add(self.panel_directory, (row, 0), (1, 2), wx.ALL | wx.EXPAND, 5)

        row += 1
        sizer_panel_components.Add(self.panel_dialog, (row, 0), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel_components.Add(self.panel_options, (row, 1), (1, 1), wx.ALL | wx.EXPAND, 5)

        self.panel_components.SetSizer(sizer_panel_components)

        sizer_panel_components.AddGrowableCol(0)
        # ------------------------------------------------------------------------------------------------------------------
        sizer_panel_frame.Add(self.panel_components, row, 0)

        self.panel_frame.SetSizer(sizer_panel_frame)

        self.Layout()

    # ------------------------------------------------------------------------------------------------------------------
    def reset_view(self, evt):
        self.SetSize((1055, 640))

    def popup_dialog(self, error_message):
        print(error_message + '\n')
        dial = wx.MessageDialog(None, str(error_message),
                                'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    # ------------------------------------------------------------------------------------------------------------------
    def OnCloseWindow(self, evt):
        self.Destroy()


########################################################################################################################
class MyApp(wx.App):
    """"""

    # ------------------------------------------------------------------------------------------------------------------
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.SetIcon(wx.Icon(APP_ICON))
        self.frame.Show()
        return True


# Run
if __name__ == "__main__":
    # https://stackoverflow.com/a/16237927
    warnings.simplefilter('error', UserWarning)
    app = MyApp(0)
    app.MainLoop()
