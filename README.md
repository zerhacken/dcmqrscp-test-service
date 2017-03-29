# dcmqrscp for integration testing

Notes on howto use dcmqrscp as a possible integration test layer.
The overall idea is to *exploit* dcmqrscp from DCMTK, start with an empty
repository add files using storescu, and then test query (C-FIND) retrieve (C-MOVE)
against a *local* repository.

## start dcmqrscp
rcp@radon dcmqrscp --log-level trace --config db/dcmqrscp.cfg  
rcp@radon echoscu -d localhost 5678 -aec STORAGE  

## send mono2.dcm to SCP
rcp@radon storescu -v --aetitle SCP --call STORAGE localhost 5678 sample/mono2.dcm  

## query SCP
rcp@radon findscu -v -S localhost 5678 --aetitle SCP --call STORAGE -k QueryRetrieveLevel=STUDY -k StudyDate -k StudyDescription -k StudyInstanceUID  

## retrieve StudyInstanceUID=072495.0449
rcp@radon movescu -v -S -aec STORAGE -aet SCP -aem SCU --port 5679 localhost 5678 -od temp -k QueryRetrieveLevel=STUDY -k StudyInstanceUID=072495.0449  

## TODO
use [wlmscpfs](http://support.dcmtk.org/docs/wlmscpfs.html) to create a worklist server.  

### worklist database config
DCMTK\dcmwlm\data\wlistdb\OFFIS
rcp@radon dump2dcm wklist1.dump wklist1.wl
DCMTK\dcmwlm\data\wlistqry
rcp@radon dump2dcm wlistqry0.dump wlistqry0.dcm

### start worklist service
wlmscpfs.exe -v -dfp worklist 5680

### *query*
findscu -v --call OFFIS localhost 5680 wlistqry0.dcm

## Related
* [dcmtk](http://dicom.offis.de/dcmtk.php.en) - DCMTK toolkit
* [dcmqrscp](http://support.dcmtk.org/docs/dcmqrscp.html) - dcmqrscp
* [dcmqrscp config](http://support.dcmtk.org/docs/file_dcmqrset.html) - config of dcmqrscp
* [findscu](http://support.dcmtk.org/docs/findscu.html) - findscu
* [movescu](http://support.dcmtk.org/docs/movescu.html) - movescu
* [storescu](http://support.dcmtk.org/docs/storescu.html) - storescu
