#!/usr/bin/python3

import sys, os
import fileinput
from pprint import pprint
import cortex

sections = cortex.parse(fileinput.input())
blocks = []
for typename, header, lines in sections:
    # print("Parsing [%s] section.." % typename)
    if typename == "enum":
        blocks.append(cortex.parse_enum(header, lines))
    elif typename == "packet":
        blocks.append(cortex.parse_packet(header, lines))
    elif typename == "flags":
        pass

pprint(blocks)
