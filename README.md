# dcmqrscp for integration testing

Notes on howto use dcmqrscp as a possible integration test layer.
The overall idea is to *exploit* dcmqrscp from DCMTK, start with an empty
repository add files using storescu, and then test query (C-FIND) retrieve (C-MOVE)
against a *local* repository.

## start dcmqrscp
rcp@radon dcmqrscp --log-level trace --config db/dcmqrscp.cfg  
rcp@radon echoscu -d localhost 5678 -aec STORAGE  

## send redmond.dcm to SCP
rcp@radon storescu -v --aetitle SCP --call STORAGE localhost 5678 sample/mono2.dcm  

## query SCP
rcp@radon findscu -v -S localhost 5678 --aetitle SCP --call STORAGE -k QueryRetrieveLevel=STUDY -k StudyDate -k StudyDescription -k StudyInstanceUID  

## retrieve StudyInstanceUID=072495.0449
rcp@radon movescu -v -S -aec STORAGE -aet SCP -aem SCU --port 5679 localhost 5678 -od temp -k QueryRetrieveLevel=STUDY -k StudyInstanceUID=072495.0449  

## Related
* [dcmtk](http://dicom.offis.de/dcmtk.php.en) - DCMTK toolkit
* [dcmqrscp](http://support.dcmtk.org/docs/dcmqrscp.html) - dcmqrscp
* [dcmqrscp config](http://support.dcmtk.org/docs/file_dcmqrset.html) - config of dcmqrscp
* [findscu](http://support.dcmtk.org/docs/findscu.html) - findscu
* [movescu](http://support.dcmtk.org/docs/movescu.html) - movescu
* [storescu](http://support.dcmtk.org/docs/storescu.html) - storescu