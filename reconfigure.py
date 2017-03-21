import urllib2
import zipfile
import tarfile
import subprocess
import sys

# sys.platform == "win32"
filename_osx = "dcmtk-3.6.0-mac-i686-static.tar.bz2"
filename_win32 = "dcmtk-3.6.0-win32-i386.zip"

url = "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/bin/"

with open(filename_win32 if sys.platform == "win32" else filename_osx ,'wb') as f:
  f.write(urllib2.urlopen(url + filename_osx).read())
  f.close()

if sys.platform == "win32":
    with zipfile.ZipFile(filename_win32, "r") as z:
        z.extractall("temp")
else:
    with tarfile.open(filename_osx) as tar:
        tar.extractall("temp")

# dcmqrscp --log-level trace --config db/dcmqrscp.cfg
# win32 temp/dcmtk-3.6.0-win32-i386/bin
# macOS temp/dcmtk-3.6.0-mac-i686-dynamic/bin
if sys.platform == "win32":
    subprocess.call(["temp/dcmtk-3.6.0-win32-i386/bin/dcmqrscp --log-level trace --config db/dcmqrscp.cfg"], shell=True)
else:
	subprocess.call(["temp/dcmtk-3.6.0-mac-i686-dynamic/bin/dcmqrscp --log-level trace --config db/dcmqrscp.cfg"], shell=True)