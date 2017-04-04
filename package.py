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
                response = urllib2.urlopen(url + "/"+ filename)
                f.write(response.read())
                f.close()
        # On-demand unpack.
        self._unpack(filename)
    def _unpack(self, filename):
        if sys.platform == "win32":
            self._unpack_zip(filename)
        else:
            self._unpack_tar(filename)
    def _unpack_zip(self, filename):
        with zipfile.ZipFile(filename, "r") as z:
            self._folder = "temp/" + z.infolist()[0].filename
            if os.path.exists(self._folder) != True:
                z.extractall("temp")
    def _unpack_tar(self, filename):
        with tarfile.open(filename, "r") as tar:
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
