#!/usr/bin/python3

import re

from .grammar import *

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
            comment.append(docline.group(1).strip())
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

