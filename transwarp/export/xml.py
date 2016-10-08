import io
import sys
import lxml.etree as ET

def dump(elem):
    print(ET.tostring(elem, encoding="unicode", pretty_print=True), end="")

def new_from_obj(obj):
    tag = ET.Element(obj.__class__.__name__.lower())
    tag.attrib["name"] = obj.name
    return tag

def gen_type(type):
    tag = new_from_obj(type)
    if type._args:
        for arg in type._args:
            tag.append(gen_type(arg))
    return tag

def gen_enum_or_flag(obj):
    tag = new_from_obj(obj)
    for field in obj.fields:
        ftag = ET.Element("field")
        ftag.attrib["name"] = field.name
        ftag.attrib["value"] = field.aligned_hex_value
        tag.append(ftag)
    return tag

def gen_struct_field(field):
    tag = new_from_obj(field)
    tag.append(gen_type(field.type))
    return tag

def gen_struct(struct):
    tag = new_from_obj(struct)
    for line in struct.comment:
        tag.append(ET.Comment(line))
    for field in struct.fields:
        for line in field.comment:
            tag.append(ET.Comment(line))
        tag.append(gen_struct_field(field))
    return tag

def export(data):
    out = io.StringIO()
    root = ET.Element("root")
    warning = "---- NON-FINALIZED FORMAT. EXPECT THIS FORMAT TO CHANGE WITHOUT WARNING ----"
    root.append(ET.Comment(warning))
    for typename, values in data.items():
        for value in values:
            for line in getattr(value, "comment", []):
                root.append(ET.Comment(line))
            if typename == "packet":
                for field in value.fields:
                    root.append(gen_struct(field))
            elif typename in ("enum", "flags"):
                root.append(gen_enum_or_flag(value))
            elif typename in ("struct", "parser", "object"):
                root.append(gen_struct(value))
            else:
                print("Unknown type tag: %s" % typename)
    root.append(ET.Comment(warning))
    dump(root)
