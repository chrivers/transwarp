#!/usr/bin/python3

import sys, os
import fileinput
from pprint import pprint
import cortex

sections = cortex.parse(fileinput.input())
enums, packets, structs = [], [], []
for typ, header, lines, comment in sections:
    # print("Parsing [%s] section.." % typ)
    if typ == "enum":
        enums.append(cortex.parse_enum(header, lines))
    elif typ == "packet":
        packets.append(cortex.parse_packet(header, lines))
    elif typ == "struct":
        structs.append(cortex.parse_struct(header, lines))
    elif typ == "flags":
        pass
    else:
        print("Unknown section type [%s]" % typ)

def section(name):
    print(("[ %s ]" % name).center(80, "-"))

section("enums")
pprint(enums)
section("packets")
pprint(packets)
section("structs")
pprint(structs)
