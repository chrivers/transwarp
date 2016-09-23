#!/usr/bin/python3

import sys, os
import re
import fileinput
from pprint import pprint

RE_BLANK   = re.compile("^\s+$")
RE_SECTION = re.compile("^(\w+)\s+(.*)")
RE_FIELD   = re.compile("^    (.*)")

def parse_enum(header, lines):
    RE_ENUM_FIELD = re.compile("(\w+)\s*=\s*(\w+)")
    fields = []
    for line in lines:
        field = RE_ENUM_FIELD.match(line)
        name, value = field.groups()
        fields.append((name, int(value, 0)))
    return fields

def parse(lines):
    sections = []
    def nextline():
        try:
            return next(lines)
        except StopIteration:
            return ""

    line = nextline()

    while line:
        if RE_BLANK.match(line):
            line = next(lines)
            continue

        section = RE_SECTION.search(line)
        if section:
            section_lines = []
            while line:
                line = nextline()
                if RE_BLANK.match(line):
                    continue

                field = RE_FIELD.match(line)
                if field:
                    section_lines.append(field.group(1))
                else:
                    typename, header = section.groups()
                    sections.append((typename, header, section_lines))
                    break
        else:
            raise ValueError("Unknown line: %r" % line)
    return sections

sections = parse(fileinput.input())
blocks = []
for typename, header, lines in sections:
    print("Parsing [%s] section.." % typename)
    if typename == "enum":
        blocks.append(parse_enum(header, lines))
    elif typename == "flags":
        pass

pprint(blocks)
