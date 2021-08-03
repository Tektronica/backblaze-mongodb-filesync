from PIL import Image, IptcImagePlugin
from PIL.ExifTags import TAGS
from settings import BACKBLAZE_URL_HEAD

class fileObj():
    def __init__(self, album, filename, bucketPath, localPath):
        self.album = album
        self.filename = filename
        self.bucketPath = bucketPath
        self.localPath = localPath

class jpgObj():
    def __init__(self, fileObj):
        self.exif = None
        self.iptc = None

        self.album = fileObj.album
        self.filename = fileObj.filename
        self.bucketPath = fileObj.bucketPath
        self.localPath = fileObj.localPath
        self.url = BACKBLAZE_URL_HEAD + self.bucketPath

        self.thumbnailUrl = ''
        self.lens = ''
        self.date = ''
        self.b2id = ''

        self.title = ''
        self.description = ''

        self._readEXIF()

    def _readEXIF(self):

        # read the image data using PIL
        image = Image.open(self.localPath)

        # extract EXIF and IPTC data from image
        # exifdata = image.getexif()

        # iterating over all EXIF data fields
        self.exif = {
            TAGS[k]: v
            for k, v in image._getexif().items()
            if k in TAGS
        }

        # https://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#synchronising-iim-elements-with-existing-xmp-properties
        # {'title':'title', 'description':'<description>'} --> 
        # {(2, 5): b'<this is some title>', (2, 120): b'<this is some description>'}
        self.iptc = IptcImagePlugin.getiptcinfo(image)  # dictionary containing IIM spec keys to binary values 

        self.date = self.get_exif_by_key('DateTimeOriginal', 'CreateDate')
        self.lens = self.get_exif_by_key('LensModel', 'LensInfo')

        if self.iptc:
            self.title = self.get_iptc_by_key((2, 5))  # title (2, 5)
            self.description = self.get_iptc_by_key((2, 120))  # description (2, 120)

        else:
            print(" This image has no iptc info")
        
        return True

    def get_exif_by_key(self, key, alt_key=''):
        # first attempt using first key
        try:
            return self.exif[key]
        except KeyError:
            pass  # Fallback to alt_key
        
        # second attempt using second key
        try:
            return self.exif[alt_key]
        except KeyError:
            print('KeyError in requesting exif key. Returning empty string.')
            return ''

    def get_iptc_by_key(self, key, alt_key=''):
        # first attempt using first key
        try:
            return self.iptc[key].decode('utf-8')
        except KeyError:
            print('KeyError in requesting iptc by key. Returning empty string.')
            return ''

    def getEXIF(self):
        return self.exif

    def getPackage(self):
        # backblaze image information needed for upload (filename is actually not needed)
        b2File = {
            'filename': self.filename,
            'localpath': self.localPath,
            'bucketpath': self.bucketPath
            }

        # document sent to MongoDB
        meta_doc = {
            'album': self.album,
            'filename': self.filename,
            'title': self.title,
            'description': self.description,
            'bucketpath': self.bucketPath,
            'url': self.url,
            'thumbnailurl': self.thumbnailUrl,
            'lens': self.lens,
            'date': self.date,
            'b2id': self.b2id
        }
        return b2File, meta_doc
