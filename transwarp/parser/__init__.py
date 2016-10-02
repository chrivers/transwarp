from transwarp.util.data import SearchableList
from transwarp.parser.parser import parse_lines
from transwarp.types.enum import Enum, Flags
from transwarp.types.struct import Struct
from transwarp.types.parser import Parser
from transwarp.types.packet import Packet
from transwarp.types.object import Object

def parse(lines):
    parsers = {
        "enum": Enum,
        "flags": Flags,
        "packet": Packet,
        "struct": Struct,
        "object": Object,
        "parser": Parser,
    }

    items = parse_lines(lines)

    res = {}
    for typ, header, section_lines, section_comment in items:
        if typ in parsers:
            parser = parsers[typ]
            if not typ in res:
                res[typ] = SearchableList()
            res[typ].append(parser(header, section_lines, section_comment))
        else:
            raise ValueError("Unknown type [%s]" % typ)
    return res
