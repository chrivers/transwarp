from .data import SearchableList
from .parser import parse_lines
from .enum import Enum, Flags
from .struct import Struct
from .packet import Packet

def parse(lines):
    parsers = {
        "enum": Enum,
        "flags": Flags,
        "packet": Packet,
        "struct": Struct,
        "object": Struct,
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
