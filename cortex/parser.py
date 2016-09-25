#!/usr/bin/python3

import re

from .enum import Enum

RE_BLANK   = re.compile("^\s+$|^\s*##.*")
RE_DOC     = re.compile("^#([^#].*)$")
RE_SECTION = re.compile("^(\w+)\s*(.*)$")
RE_FIELD   = re.compile("^    (.*)")

def parse_packet(header, lines, comment):
    return (header, [parse_struct(c[0], c[2], c[3]) for c in parse_lines(iter(lines))], comment)

def parse_struct(header, lines, comment):
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
    return (header, fields, comment)

def parse_lines(lines):
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

def parse(lines):
    parsers = {
        "enum": Enum,
        "flags": Enum,
        "packet": parse_packet,
        "struct": parse_struct,
    }

    items = parse_lines(lines)

    res = {}
    for typ, header, section_lines, section_comment in items:
        if typ in parsers:
            parser = parsers[typ]
            res.setdefault(typ, []).append(parser(header, section_lines, section_comment))
        else:
            print("Unknown type [%s]" % typ)
    return res
