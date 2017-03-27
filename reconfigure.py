import urllib2
import zipfile
import tarfile
import subprocess
import sys
import os
import time
from threading import Timer
from signal import *

# HACKME unix only (i.e dicom.dic burned into Windows binary)
org = os.getenv("DCMDICTPATH")

def clean(*args):
    # restore DCMDICTPATH
    os.environ['DCMDICTPATH'] = org
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

def unpack(filename):
    if sys.platform == "win32":
        with zipfile.ZipFile(filename, "r") as z:
            z.extractall("temp")
            os.remove(filename)
    else:
        with tarfile.open(filename) as tar:
            tar.extractall("temp")
            os.remove(filename)

def installDCMTK(filename):
    url = "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/bin/"
    # On-demand download
    if os.path.isfile(filename) != True:
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(url + filename).read())
            f.close()
    # On-demand unpack
    folder = "temp/dcmtk-3.6.0-win32-i386" if sys.platform == "win32" else "temp/dcmtk-3.6.0-mac-i686-dynamic"
    if os.path.exists(folder) != True:
        unpack(filename)

def storage():
    local = "temp/dcmtk-3.6.0-mac-i686-dynamic/bin/"
    # storescu -v --aetitle SCP --call STORAGE localhost 5678 sample/mono2.dcm
    for dcm in os.listdir("sample"):
        print("uploading: " + "sample/" + dcm)
        subprocess.call([local + "storescu", "-v", "--aetitle", "SCP", "--call", "STORAGE", "localhost", "5678", "sample/" + dcm])

def main():
    # cleanup storage
    for filename in os.listdir("db/storage"):
        if filename.endswith(tuple([".dcm", ".dat"])):
            print("removed: " + "db/storage/" + filename)
            os.remove("db/storage/" + filename)

    # DCMTK binaries
    filename = "dcmtk-3.6.0-win32-i386.zip" if sys.platform == "win32" else "dcmtk-3.6.0-mac-i686-static.tar.bz2"
    installDCMTK(filename)

    os.environ["DCMDICTPATH"] = os.getcwd() + "/temp/dcmtk-3.6.0-mac-i686-dynamic/share/dcmtk/dicom.dic"

    # delayed background upload of sample folder
    t = Timer(3.0, storage)
    t.start()

    # dcmqrscp --log-level trace --config db/dcmqrscp.cfg
    # win32 temp/dcmtk-3.6.0-win32-i386/bin
    # macOS temp/dcmtk-3.6.0-mac-i686-dynamic/bin
    if sys.platform == "win32":
        subprocess.call(["temp/dcmtk-3.6.0-win32-i386/bin/dcmqrscp --config db/dcmqrscp.cfg"])
    else:
        subprocess.call(["temp/dcmtk-3.6.0-mac-i686-dynamic/bin/dcmqrscp", "--config", "db/dcmqrscp.cfg"])

if __name__ == "__main__":
    main()
