import urllib2
import zipfile
import tarfile
import subprocess
import sys
import os
import time
import glob

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
    else:
        with tarfile.open(filename) as tar:
            tar.extractall("temp")

def dcmtkPackage():
    return "dcmtk-3.6.0-win32-i386.zip" if sys.platform == "win32" else "dcmtk-3.6.0-mac-i686-static.tar.bz2"

def dcmtkRootFolder():
    return "temp/dcmtk-3.6.0-win32-i386" if sys.platform == "win32" else "temp/dcmtk-3.6.0-mac-i686-dynamic"

def dcmtkBinaryFolder():
    return dcmtkRootFolder() + "/bin"

def storageFolder():
    return "db/storage"

def installDCMTK(filename):
    url = "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/bin/"
    # On-demand download.
    if os.path.isfile(filename) != True:
        print("Downloading " + filename)
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(url + filename).read())
            f.close()
    # On-demand unpack.
    if os.path.exists(dcmtkRootFolder()) != True:
        print("Unpacking " + filename)
        unpack(filename)

def transferSampleFiles():
    # storescu -v --aetitle SCP --call STORAGE localhost 5678 sample/mono2.dcm
    for dcm in os.listdir("sample"):
        subprocess.call([dcmtkBinaryFolder() + "/" + "storescu", "-v", "--aetitle", "SCP", "--call", "STORAGE", "localhost", "5678", "sample/" + dcm])

def main():
    # Cleanup storage
    for filename in os.listdir(storageFolder()):
        if filename.endswith(tuple([".dcm", ".dat"])):
            print("Removing: " + storageFolder() + "/" + filename)
            os.remove(storageFolder() + "/" + filename)

    # DCMTK binaries
    installDCMTK(dcmtkPackage())
    
    os.environ["DCMDICTPATH"] = os.getcwd() + "/" + dcmtkRootFolder() + "/share/dcmtk/dicom.dic"

    # Delayed background upload of files in sample folder.
    t = Timer(3.0, transferSampleFiles)
    t.start()

    # dcmqrscp --log-level trace --config db/dcmqrscp.cfg
    # win32 temp/dcmtk-3.6.0-win32-i386/bin
    # macOS temp/dcmtk-3.6.0-mac-i686-dynamic/bin
    subprocess.call([dcmtkBinaryFolder() + "/" + "dcmqrscp", "--config", "db/dcmqrscp.cfg"])

if __name__ == "__main__":
    main()
