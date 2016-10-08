import io
import sys
#import lxml.etree.ElementTree as ET
import lxml.etree as ET

def dump(elem):
    print(ET.tostring(elem, encoding="unicode", pretty_print=True), end="")

def export(data):
    out = io.StringIO()
    root = ET.Element("root")
    for typename, values in data.items():
        for value in values:
            typetag = ET.Element(typename)
            typetag.attrib["name"] = value.name
            root.append(typetag)
            for line in getattr(value, "comment", []):
                typetag.append(ET.Comment(line))
            for field in getattr(value, "fields", []):
                fieldtag = ET.Element("field")
                for line in getattr(field, "comment", []):
                    fieldtag.append(ET.Comment(line))
                fieldtag.attrib["name"] = field.name
                if hasattr(field, "type"):
                    fieldtag.attrib["type"] = str(field.type)
                if hasattr(field, "value"):
                    fieldtag.attrib["value"] = field.value
                typetag.append(fieldtag)
    dump(root)
