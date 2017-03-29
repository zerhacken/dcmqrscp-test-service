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
from package import TemporaryPackage

# HACKME unix only (i.e dicom.dic burned into Windows binary)
org = os.getenv("DCMDICTPATH")

def clean(*args):
    # restore DCMDICTPATH
    os.environ['DCMDICTPATH'] = org
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

def dcmtkPackage():
    return "dcmtk-3.6.0-win32-i386.zip" if sys.platform == "win32" else "dcmtk-3.6.0-mac-i686-static.tar.bz2"

def dcmtkURL():
    return "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/bin/"

def dcmtkRootFolder():
    return "temp/dcmtk-3.6.0-win32-i386" if sys.platform == "win32" else "temp/dcmtk-3.6.0-mac-i686-dynamic"

def dcmtkBinaryFolder():
    return dcmtkRootFolder() + "/bin"

def storageFolder():
    return "db/storage"

def sample():
    # storescu -v --aetitle SCP --call STORAGE localhost 5678 sample/mono2.dcm
    for filename in os.listdir("sample"):
        if filename.endswith(".dcm"):
            subprocess.call([dcmtkBinaryFolder() + "/" + "storescu", "-v", "--aetitle", "SCP", "--call", "STORAGE", "localhost", "5678", "sample/" + filename])

def wlmscpfs():
    # wlmscpfs -v -dfp worklist 5680
    subprocess.call([dcmtkBinaryFolder() + "/" + "wlmscpfs", "-v", "-dfp", "worklist", "5680"])

def dcmqrscp():
    # dcmqrscp --log-level trace --config db/dcmqrscp.cfg
    # win32 temp/dcmtk-3.6.0-win32-i386/bin
    # macOS temp/dcmtk-3.6.0-mac-i686-dynamic/bin
    subprocess.call([dcmtkBinaryFolder() + "/" + "dcmqrscp", "--config", "db/dcmqrscp.cfg"])

def main():
    # Cleanup storage
    for filename in os.listdir(storageFolder()):
        if filename.endswith(tuple([".dcm", ".dat"])):
            print("Removing: " + storageFolder() + "/" + filename)
            os.remove(storageFolder() + "/" + filename)

    # local install DCMTK binaries
    package = TemporaryPackage(dcmtkURL() + dcmtkPackage())

    os.environ["DCMDICTPATH"] = os.getcwd() + "/" + package.folder + "/share/dcmtk/dicom.dic"

    # worklist
    w = Timer(0.0, wlmscpfs)
    w.start()

    # archive
    a = Timer(0.0, dcmqrscp)
    a.start()

    # Delayed background upload of files in sample folder.
    s = Timer(3.0, wlmscpfs)
    s.start()

if __name__ == "__main__":
    main()
