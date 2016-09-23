#!/usr/bin/python3

import re

RE_BLANK   = re.compile("^\s+$|^\s*##.*")
RE_DOC     = re.compile("^#([^#].*)$")
RE_SECTION = re.compile("^(\w+)\s*(.*)$")
RE_FIELD   = re.compile("^    (.*)")

def parse_enum(header, lines):
    RE_ENUM_FIELD = re.compile("(\w+)\s*=\s*(\w+)")
    fields = []
    for line in lines:
        field = RE_ENUM_FIELD.match(line)
        name, value = field.groups()
        fields.append((name, int(value, 0)))
    return (header, fields)

def parse_case(name, lines):
    return (name, len(lines))

def parse_packet(header, lines):
    return [parse_case(c[0], c[2]) for c in parse(iter(lines))]

def parse_struct(header, lines):
    RE_STRUCT_FIELD = re.compile("(\w+):\s*(.*)")
    fields = []
    comment = []
    for line in lines:
        doc = RE_DOC.match(line)
        if doc:
            comment.append(doc.group(1).strip())
            continue
        field = RE_STRUCT_FIELD.match(line)
        if field:
            name, typ = field.groups()
            fields.append((name, typ, comment))
            comment = []
    return (header, fields)

def parse(lines):
    def nextline(lines):
        try:
            return next(lines)
        except StopIteration:
            return ""

    sections = []
    comment = []
    line = nextline(lines)
    while line:
        if RE_BLANK.match(line):
            line = nextline(lines)
            continue
        docline = RE_DOC.match(line)
        if docline:
            comment.append(docline.group(1))
            line = nextline(lines)
            continue

        section = RE_SECTION.search(line)
        if section:
            section_comment = comment[:]
            section_lines = []
            comment = []
            while line:
                line = nextline(lines)
                if RE_BLANK.match(line):
                    continue

                field = RE_FIELD.match(line)
                if field:
                    section_lines.append(field.group(1))
                else:
                    typ, header = section.groups()
                    sections.append((typ, header, section_lines, section_comment))
                    break
            continue
        else:
            raise ValueError("Unknown line: %r" % line)
    return sections

def organize(items):
    res = {}
    for tup in items:
        res.setdefault(tup[0], []).append(tup[1:])
    return res
