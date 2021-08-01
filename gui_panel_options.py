from backblaze import Backblaze
from mongodb import Collection
from settings import APPLICATION_KEY_ID, APPLICATION_KEY, KEY_NAME, USERNAME, PASSWORD, DATABASE

import wx
from file_objects import jpgObj

class Options(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        # instance variables -------------------------------------------------------------------------------------------
        self.parent = parent
        self.frame = frame
        self.packaged_b2Files = []
        self.packaged_MongoDocs = []

        # PANELS =======================================================================================================
        self.panel_components = wx.Panel(self, wx.ID_ANY)

        # COMPONENTS ===================================================================================================
        self.btn_prepare_pkg = wx.Button(self, wx.ID_ANY, "Prepare Package")
        self.Bind(wx.EVT_BUTTON, self.package, self.btn_prepare_pkg)
        
        self.btn_upload = wx.Button(self, wx.ID_ANY, "Upload")
        self.Bind(wx.EVT_BUTTON, self.upload, self.btn_upload)

        # LAYOUT =======================================================================================================
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(209, 213, 219))

    def __do_layout(self):
        sizer_panel_components= wx.GridBagSizer(0, 0)

        # COMPONENTS  --------------------------------------------------------------------------------------------------
        row = 0
        label_1 = wx.StaticText(self, wx.ID_ANY, "OPTIONS")
        label_1.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_panel_components.Add(label_1, (row, 0), (1, 3), 0, 0)

        row += 1
        sizer_panel_components.Add(self.btn_prepare_pkg, (row, 0), (1, 2), wx.ALL, 5)

        row += 1
        sizer_panel_components.Add(self.btn_upload, (row, 0), (1, 2), wx.ALL, 5)

        row += 1
        # ...

        # sizer_panel_main.AddGrowableRow(0)
        # sizer_panel_main.AddGrowableCol(1)

        self.SetSizer(sizer_panel_components)
        self.Layout()
    
    def package(self, evt):
        if self.frame is not None:
            files = self.frame.panel_dialog.getCheckedObjects()

            self.packaged_b2Files = []
            self.packaged_MongoDocs = []

            for fileObj in files:
                imgObj = jpgObj(fileObj)
                b2File, meta_doc = imgObj.getPackage()

                self.packaged_b2Files = self.packaged_b2Files + [b2File]
                self.packaged_MongoDocs = self.packaged_MongoDocs + [meta_doc]
        else:
            pass

    def upload(self, evt):
        if self.packaged_b2Files == [] or self.packaged_MongoDocs == []:
            print('\nPackage files for upload first!')
            return False
        else:
            # BACKBLAZE -------------------------------------------------------------

            backblazeObj = Backblaze(APPLICATION_KEY_ID, APPLICATION_KEY)
            bucketObj = backblazeObj.get_bucket(KEY_NAME)

            print(f'\nReviewing current file list in {KEY_NAME} bucket')
            print(bucketObj.list_files())

            print('\nUploading to Backblaze B2 Bucket')
            res, FileVersions = bucketObj.upload_to_bucket(self.packaged_b2Files)

            if res:
                print('Completed upload to Backblaze Bucket')
            else:
                print('[UPLOAD FAILED] uploade to Backblaze Bucket has failed!')
                return False

            for row, fileVersion in enumerate(FileVersions):
                self.packaged_MongoDocs[row]['b2id'] = fileVersion.id_

            # MONGODB ---------------------------------------------------------------
            print('\nUpdating database documents on MongoDB')
            col = 'gallery'
            colObj = Collection(USERNAME, PASSWORD, DATABASE, col)
            res, ids = colObj.insert(self.packaged_MongoDocs)

            if res:
                print('Completed document update to MongoDB database!')
                for id in ids:
                    print(id)
            else:
                print('[UPLOAD FAILED] document update to MongoDB database failed!')
                return False
            
            return True



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1028, 278))
        self.panel_main = wx.Panel(self, wx.ID_ANY)
        self.panel_dialog = Options(self.panel_main, None)

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
