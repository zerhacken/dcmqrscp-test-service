import os
import sys
import urllib2
import zipfile
import tarfile

class TemporaryPackage(object):
    def __init__(self, raw):
        self._url, self._filename = os.path.split(raw)
        self._install(self.url, self.filename)
    def _install(self, url, filename):
        # On-demand download.
        if os.path.isfile(filename) != True:
            with open(filename,'wb') as f:
                f.write(urllib2.urlopen(url + "/"+ filename).read())
                f.close()
        # On-demand unpack.
        self._unpack(filename)
    def _unpack(self, filename):
        if sys.platform == "win32":
            with zipfile.ZipFile(filename, "r") as z:
                z.extractall("temp")
        else:
            with tarfile.open(filename) as tar:
                self._folder = "temp/" + tar.getmembers()[0].name
                if os.path.exists(self._folder) != True:
                    tar.extractall("temp")
    @property
    def url(self):
        return self._url
    @property
    def filename(self):
        return self._filename
    @property
    def folder(self):
        return self._folder