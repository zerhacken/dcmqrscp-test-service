import xml.etree.cElementTree as ET

def worklist():
    root = ET.Element("file-format")

    #<meta-header xfer="1.2.840.10008.1.2.1" name="Little Endian Explicit">
    doc = ET.SubElement(root, "meta-header", xfer="1.2.840.10008.1.2.1", name="Little Endian Explicit")

    #<element tag="0002,0000" vr="UL" vm="1" len="4" name="FileMetaInformationGroupLength">200</element>
    #<element tag="0002,0001" vr="OB" vm="1" len="2" name="FileMetaInformationVersion" binary="hidden"></element>
    #<element tag="0002,0002" vr="UI" vm="1" len="26" name="MediaStorageSOPClassUID">1.2.276.0.7230010.3.1.0.1</element>
    #<element tag="0002,0003" vr="UI" vm="1" len="56" name="MediaStorageSOPInstanceUID">1.2.276.0.7230010.3.1.4.3281700972.12996.1490774444.649</element>
    #<element tag="0002,0010" vr="UI" vm="1" len="20" name="TransferSyntaxUID">1.2.840.10008.1.2.1</element>
    #<element tag="0002,0012" vr="UI" vm="1" len="28" name="ImplementationClassUID">1.2.276.0.7230010.3.0.3.6.0</element>
    #<element tag="0002,0013" vr="SH" vm="1" len="16" name="ImplementationVersionName">OFFIS_DCMTK_360</element>
    ET.SubElement(doc, "element", tag="0002,0000", vr="UL", vm="1", len="4", name="FileMetaInformationGroupLength").text = "200"
    ET.SubElement(doc, "element", tag="0002,0001", vr="OB", vm="1", len="2", name="FileMetaInformationVersion", binary="hidden").text = ""
    ET.SubElement(doc, "element", tag="0002,0002", vr="UI", vm="1", len="26", name="MediaStorageSOPClassUID").text = "1.2.276.0.7230010.3.1.0.1"
    ET.SubElement(doc, "element", tag="0002,0003", vr="UI", vm="1", len="56", name="MediaStorageSOPInstanceUID").text = "1.2.276.0.7230010.3.1.4.3281700972.12996.1490774444.649"
    ET.SubElement(doc, "element", tag="0002,0010", vr="UI", vm="1", len="20", name="TransferSyntaxUID").text = "1.2.840.10008.1.2.1"
    ET.SubElement(doc, "element", tag="0002,0012", vr="UI", vm="1", len="28", name="ImplementationClassUID").text = "1.2.276.0.7230010.3.0.3.6.0"
    ET.SubElement(doc, "element", tag="0002,0013", vr="SH", vm="1", len="16", name="ImplementationVersionName").text = "OFFIS_DCMTK_360"

    #<data-set xfer="1.2.840.10008.1.2.1" name="Little Endian Explicit">
    doc = ET.SubElement(root, "data-set", xfer="1.2.840.10008.1.2.1", name="Little Endian Explicit")

    #<element tag="0008,0005" vr="CS" vm="1" len="10" name="SpecificCharacterSet">ISO_IR 100</element>
    #<element tag="0008,0050" vr="SH" vm="1" len="6" name="AccessionNumber">1234</element>
    #<element tag="0010,0010" vr="PN" vm="1" len="16" name="PatientName">PEDERSEN^RASMUS</element>
    #<element tag="0010,0020" vr="LO" vm="1" len="8" name="PatientID">230179</element>
    #<element tag="0010,0030" vr="DA" vm="1" len="8" name="PatientBirthDate">19790123</element>
    #<element tag="0010,0040" vr="CS" vm="1" len="2" name="PatientSex">M</element>
    #<element tag="0010,2000" vr="LO" vm="1" len="10" name="MedicalAlerts">hacksager</element>
    #<element tag="0010,2110" vr="LO" vm="1" len="6" name="Allergies">java</element>
    #<element tag="0020,000d" vr="UI" vm="1" len="26" name="StudyInstanceUID">1.2.276.0.7230010.3.2.101</element>
    #<element tag="0032,1032" vr="PN" vm="1" len="6" name="RequestingPhysician">smith</element>
    #<element tag="0032,1060" vr="LO" vm="1" len="6" name="RequestedProcedureDescription">hack</element>
    ET.SubElement(doc, "element", tag="0008,0005", vr="CS", vm="1", len="10", name="SpecificCharacterSet").text = "ISO_IR 100"
    ET.SubElement(doc, "element", tag="0008,0050", vr="SH", vm="1", len="6", name="AccessionNumber").text = "1234"
    ET.SubElement(doc, "element", tag="0010,0010", vr="PN", vm="1", len="16", name="PatientName").text = "PEDERSEN^RASMUS"
    ET.SubElement(doc, "element", tag="0010,0020", vr="LO", vm="1", len="8", name="PatientID").text = "230179"
    ET.SubElement(doc, "element", tag="0010,0030", vr="DA", vm="1", len="8", name="PatientBirthDate").text = "19790123"
    ET.SubElement(doc, "element", tag="0010,0040", vr="CS", vm="1", len="2", name="PatientSex").text = "M"
    ET.SubElement(doc, "element", tag="0010,2000", vr="LO", vm="1", len="10", name="MedicalAlerts").text = "hacksager"
    ET.SubElement(doc, "element", tag="0010,2110", vr="LO", vm="1", len="6", name="Allergies").text = "java"
    ET.SubElement(doc, "element", tag="0020,000d", vr="UI", vm="1", len="26", name="StudyInstanceUID").text = "1.2.276.0.7230010.3.2.101"
    ET.SubElement(doc, "element", tag="0032,1032", vr="PN", vm="1", len="6", name="RequestingPhysician").text = "smith"
    ET.SubElement(doc, "element", tag="0032,1060", vr="LO", vm="1", len="6", name="RequestedProcedureDescription").text = "hack"

    #<sequence tag="0040,0100" vr="SQ" card="1" len="176" name="ScheduledProcedureStepSequence">

    tree = ET.ElementTree(root)

    return tree

def main():
    tree = worklist();
    tree.write("hack.xml")

if __name__ == "__main__":
    main()
