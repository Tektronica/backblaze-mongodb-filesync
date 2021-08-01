import wx
import wx.lib.agw.ultimatelistctrl as ULC
from ObjectListView2 import ObjectListView, ColumnDefn
import sys
from file_objects import fileObj
import os
import glob
import time
import time

# http://objectlistview.sourceforge.net/cs/features.html#checkboxes-in-any-column
# http://objectlistview.sourceforge.net/cs/recipes.html#recipe-checkbox
# http://objectlistview.sourceforge.net/python/recipes.html

class Dialog(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        # instance variables -------------------------------------------------------------------------------------------
        self.parent = parent
        self.frame = frame
        self.path_to_root = os.path.dirname(os.path.realpath(__file__))
        print('working directory:', self.path_to_root)
        self.files = []

        # PANELS =======================================================================================================
        self.panel_components = wx.Panel(self, wx.ID_ANY)

        # COMPONENTS ===================================================================================================
        self.combo_file_extension = wx.ComboBox(
            self, wx.ID_ANY, choices=['jpg', 'png', 'md'])
        self.Bind(wx.EVT_COMBOBOX, self.update_tree, self.combo_file_extension)

        self.fileList = ObjectListView(self, wx.ID_ANY,
                                       sortable=False,
                                       useAlternateBackColors=False,
                                       style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.reportEvent, self.fileList.checkStateColumn)


        # LAYOUT =======================================================================================================
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(249, 168, 212))

        self.combo_file_extension.SetSelection(0)

        fileNameCol = ColumnDefn("File", "left", width=300, valueGetter="filename")
        self.fileList.InstallCheckStateColumn(fileNameCol)
        self.fileList.SetColumns([
            fileNameCol,
            ColumnDefn("Bucket Path", "left", width=400, valueGetter="bucketPath"),
            ColumnDefn("Local Path", "left", width=400, valueGetter="localPath")
        ])

        self.fileList.SetMinSize((1050, 400))  # length, width

    def __do_layout(self):
        sizer_panel_components = sizer_panel_components = wx.GridBagSizer(0, 0)
        sizer_panel_components.AddGrowableCol(0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        label_1 = wx.StaticText(self, wx.ID_ANY, "DIALOG")
        label_1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT,
                        wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_panel_components.Add(label_1, (row, 0), (1, 2), wx.ALL, 5)

        row += 1
        sizer_panel_components.Add(
            self.combo_file_extension, (row, 0), (1, 1), wx.ALL, 5)

        row += 1
        sizer_panel_components.Add(
            self.fileList, (row, 0), (1, 2), wx.ALL | wx.EXPAND, 5)

        row += 1
        # ...

        self.SetSizer(sizer_panel_components)
        self.Layout()

    def populate(self):
        normal_path = os.path.normpath(self.path_to_root)
        root = os.path.basename(normal_path)
        f_ext = self.combo_file_extension.GetValue()  # file extension
        paths = list(glob.iglob(self.path_to_root +
                     f"/**/*{'.' + f_ext}", recursive=True))

        self.files = []  # removes current items from list
        for localPath in paths:
            bucketPath = localPath.split(root)[1]
            newRow = [fileObj(
                filename=os.path.basename(localPath),
                bucketPath=bucketPath,
                localPath=localPath
                )]
            self.files = self.files + newRow
        
        self.UpdateOLV()

    def UpdateOLV(self):
        """
        Remove the gap (usually intended for an icon or checkbox) in the first column of each row of an
        ObjectListView object by creating a 0 width first column.
            > https://stackoverflow.com/a/25080026/3382269
        :return:
        """
        print('Updating File List...')
        wx.CallAfter(self.fileList.SetObjects, self.files)
        wx.CallAfter(self.checkAllItems)

    def reportEvent(self, evt):
        objects = self.fileList.GetCheckedObjects()

        print(f'\n{len(objects)} selected files:')
        for obj in objects:
            print(obj.filename)
    
    def checkAllItems(self):
        wait = wx.BusyCursor()
        msg = "Loading all files into list"
        busyDlg = wx.BusyInfo(msg, parent=self.frame)

        print('Checking all items in list')
        objects = self.fileList.GetObjects()
        for obj in objects:
            # print(self.fileList.IsChecked(obj))
            self.fileList.ToggleCheck(obj)
            self.fileList.RefreshObjects(objects)

        busyDlg = None
        del wait

    def first_update(self, path):
        self.path_to_root = path
        self.populate()
        self.panel_components.Layout()

    def update_tree(self, evt):
        self.populate()
        self.panel_components.Layout()

    def getCheckedItems(self):
        checkedItems = self.fileList.GetCheckedObjects()
        items = []
        for row, obj in enumerate(checkedItems):
            items.append({
                'filename': obj.filename,
                'bucketpath': obj.bucketPath,
                'filepath': obj.localPath
            })

        return items


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1070, 500))

        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = Dialog(self.panel_main, None)

        self.btn_run = wx.Button(self, wx.ID_ANY, label="Run Test")
        self.Bind(wx.EVT_BUTTON, self.run_test, self.btn_run)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Dialog")

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_components = wx.BoxSizer(wx.VERTICAL)
        sizer_components.Add(self.btn_run, 1, wx.EXPAND, 0)

        sizer_components.Add(self.panel_dialog, 2, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_components)

        sizer_main.Add(self.panel_main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()

    def run_test(self, evt):
        path = '/Users/tektronica/Documents'
        self.panel_dialog.first_update(path)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
