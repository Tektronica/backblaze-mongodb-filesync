import wx
import wx.lib.agw.hypertreelist as HTL

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="HyperTreeList Demo")

        tree = HTL.HyperTreeList(self, agwStyle=wx.TR_DEFAULT_STYLE |
                                 HTL.TR_ELLIPSIZE_LONG_ITEMS)
        tree.AddColumn("Tree Column", width=200)
        tree.AddColumn("Column 1", width=200, flag=wx.ALIGN_LEFT)
        root = tree.AddRoot("Root")

        parent = tree.AppendItem(root, "First child")
        tree.SetItemText(parent, "Child of root", column=1)

        child = tree.AppendItem(parent, "First Grandchild")
        tree.SetItemText(child, "Column1 Text", column=1)

        child2 = tree.AppendItem(root, "Second child")
        button = wx.Button(tree.GetMainWindow(), label="Button1")
        tree.SetItemWindow(child2, button, column=1)


# our normal wxApp-derived class, as usual
app = wx.App(redirect=False)
locale = wx.Locale(wx.LANGUAGE_DEFAULT)
frame = MyFrame()
app.SetTopWindow(frame)
frame.Show()
app.MainLoop()