from PIL import Image
from PIL.ExifTags import TAGS


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
        
        return True
    
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
