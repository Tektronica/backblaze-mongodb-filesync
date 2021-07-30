import wx
import wx
import wx.lib.agw.hypertreelist as HTL
import os
import glob
import time

class Dialog(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        # instance variables -------------------------------------------------------------------------------------------
        self.parent = parent
        self.frame = frame
        self.path_to_root = os.path.dirname(os.path.realpath(__file__))
        print('working directory:', self.path_to_root)

        # PANELS =======================================================================================================
        self.panel_components = wx.Panel(self, wx.ID_ANY)

        # COMPONENTS ===================================================================================================
        self.combo_file_extension = wx.ComboBox(self, wx.ID_ANY, choices=['jpg', 'png', 'md'])
        self.Bind(wx.EVT_COMBOBOX, self.update_tree, self.combo_file_extension)

        # self.treeList = HTL.HyperTreeList(self, agwStyle=wx.TR_DEFAULT_STYLE | 0x4000)

        self.fileList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT)

        # LAYOUT =======================================================================================================
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(249, 168, 212))
        
        self.combo_file_extension.SetSelection(0)
        
        # self.treeList.AddColumn("Current Directory")
        # self.treeList.SetColumnWidth(0, 200)

        self.fileList.InsertColumn(0, "File")
        self.fileList.InsertColumn(1, "Bucket Path")
        self.fileList.InsertColumn(2, "Local Path")
        self.fileList.SetColumnWidth(0, 100)
        self.fileList.SetColumnWidth(1, 400)
        self.fileList.SetColumnWidth(2, 400)

    def __do_layout(self):
        sizer_panel_components= wx.GridBagSizer(0, 0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        label_1 = wx.StaticText(self, wx.ID_ANY, "DIALOG")
        label_1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_panel_components.Add(label_1, (row, 0), (1, 2), wx.LEFT, 5)
        
        row += 1
        sizer_panel_components.Add(self.combo_file_extension, (row, 0), (1, 1), wx.BOTTOM, 5)
        
        row += 1
        # sizer_panel_components.Add(self.treeList, (row, 0), (1, 1), wx.BOTTOM, 5)
        sizer_panel_components.Add(self.fileList, (row, 0), (1, 2), wx.ALL, 5)

        row += 1
        # ...

        # sizer_panel_main.AddGrowableRow(0)
        # sizer_panel_main.AddGrowableCol(1)

        self.SetSizer(sizer_panel_components)
        self.Layout()
    
    def populate(self):
        # https://stackoverflow.com/a/26017709
        # https://stackoverflow.com/a/25060346
        # https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/

        # for root, dirs, files in os.walk(self.path_to_root):
        #     for name in files:
        #         location = os.path.join(root, name)
        #         self.allFiles.append(location)

        normal_path = os.path.normpath(self.path_to_root)
        root = os.path.basename(normal_path)
        f_ext = self.combo_file_extension.GetValue() # file extension
        paths = list(glob.iglob(self.path_to_root + f"/**/*{'.' + f_ext}", recursive = True))

        self.fileList.DeleteAllItems()
        index = 0
        for index, localPath in enumerate(paths):
            bucketPath = localPath.split(root)[1]
            self.fileList.InsertItem(index, os.path.basename(localPath))
            self.fileList.SetItem(index, column=1, label=bucketPath)
            self.fileList.SetItem(index, column=2, label=localPath)

        # TLRoot = self.treeList.AddRoot(root, ct_type= 1)
        # self.allDirs.append(root)
        # self.allDirsItem.append(TLRoot)

        # for eachName in self.allFiles:
        #     nameSplit = eachName.split(os.sep)
        #     matchingDirFound = False

        #     lenNS = len(nameSplit)
        #     i = lenNS - 1

        #     for eachNameSplit in reversed(nameSplit):
        #         for eachDoneDir in reversed(self.allDirs):
        #             if eachNameSplit == eachDoneDir:
        #                 matchingDirFound = True
        #                 break

        #         if matchingDirFound:
        #             break
        #         i = i-1

        #     if matchingDirFound:
        #         for k in range(i, lenNS-1):
        #             self.allDirsItem.append([])
        #             self.allDirsItem[k+1] = self.treeList.AppendItem(self.allDirsItem[k], nameSplit[k+1], ct_type=1)

        #             if len(self.allDirs) > k+1:
        #                 self.allDirs[k+1] = nameSplit[k+1]
        #             else:
        #                 self.allDirs.append(nameSplit[k+1])

    def first_update(self, path):
        self.path_to_root = path
        self.populate()
        time.sleep(1)
        self.panel_components.Layout()

    def update_tree(self, evt):
        self.populate()
        self.panel_components.Layout()
    
    def getItems(self):
        items = []

        rows = self.fileList.GetItemCount()
        for row in range(rows):
            items.append({
                'filename': self.fileList.GetItemText(item=row, col=0),
                'bucketpath': self.fileList.GetItemText(item=row, col=1),
                'filepath': self.fileList.GetItemText(item=row, col=2)
            })

        return items


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1028, 278))
        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = Dialog(self.panel_main, None)

        self.__set_properties()
        self.__do_layout()
        
        path = '/Users/tektronica/Documents'
        self.panel_dialog.first_update(path)

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

