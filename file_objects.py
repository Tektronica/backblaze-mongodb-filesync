from PIL import Image
from PIL.ExifTags import TAGS

class fileObj():
    def __init__(self, filename, bucketPath, localPath):
        self.filename = filename
        self.bucketPath = bucketPath
        self.localPath = localPath

class jpgObj():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.exif = None

        self.album = ''
        self.filename = ''
        self.url = ''
        self.thumbnailUrl = ''
        self.lens = ''
        self.date = ''

        self._readEXIF()

    def _readEXIF(self):

        # read the image data using PIL
        image = Image.open(self.path_to_file)

        # extract EXIF data
        exifdata = image.getexif()

        # iterating over all EXIF data fields
        self.exif = {
            TAGS[k]: v
            for k, v in image._getexif().items()
            if k in TAGS
        }
        self.date = self.get_exif_by_key('date')
        self.lens = self.get_exif_by_key('lens')
        
        return True

    def get_exif_by_key(self, key):
        try:
            return self.exif[key]
        except KeyError:
            print('KeyError in requesting exif key. Returning empty string.')
            return ''

    def getEXIF(self):
        return self.exif

    def getDB_meta(self):
        return {
            'album': self.album,
            'filename': self.filename,
            'url': self.url,
            'thumbnailUrl': self.thumbnailUrl,
            'lens': self.lens,
            'date': self.date
        }
