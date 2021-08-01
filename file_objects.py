from PIL import Image
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

        self.album = fileObj.album
        self.filename = fileObj.filename
        self.bucketPath = fileObj.bucketPath
        self.localPath = fileObj.localPath
        self.url = BACKBLAZE_URL_HEAD + self.bucketPath

        self.thumbnailUrl = ''
        self.lens = ''
        self.date = ''
        self.b2id = ''

        self._readEXIF()

    def _readEXIF(self):

        # read the image data using PIL
        image = Image.open(self.localPath)

        # extract EXIF data
        exifdata = image.getexif()

        # iterating over all EXIF data fields
        self.exif = {
            TAGS[k]: v
            for k, v in image._getexif().items()
            if k in TAGS
        }
        self.date = self.get_exif_by_key('DateTimeOriginal', 'CreateDate')
        self.lens = self.get_exif_by_key('LensModel', 'LensInfo')
        
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

    def getEXIF(self):
        return self.exif

    def getPackage(self):
        b2File = {
            'filename': self.filename,
            'localpath': self.localPath,
            'bucketpath': self.bucketPath
            }

        meta_doc = {
            'album': self.album,
            'filename': self.filename,
            'bucketpath': self.bucketPath,
            'url': self.url,
            'thumbnailurl': self.thumbnailUrl,
            'lens': self.lens,
            'date': self.date,
            'b2id': self.b2id
        }
        return b2File, meta_doc
