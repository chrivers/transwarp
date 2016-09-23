#!/usr/bin/python3

import sys, os
import re
import fileinput

RE_BLANK   = re.compile("^\s+$")
RE_SECTION = re.compile("^(\w+)\s+(.*)")
RE_FIELD   = re.compile("^    (.*)")

def parse_enum(header, lines):
    print (header, lines)

def parse(lines):
    elements = []
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
                    elements.append((typename, header, section_lines))
                    break
        else:
            print("Unknown line: %r" % line)
            sys.exit()
    return elements

from pprint import pprint

pprint(parse(fileinput.input()), width=300)
