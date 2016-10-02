from transwarp.util.data import SearchableList
from transwarp.parser.grammar import RE_PARSER_DEF, RE_STRUCT_FIELD, RE_DOC
from transwarp.parser.strutil import text_width
from transwarp.parser.types.datatype import Type
from transwarp.parser.types.struct import Struct
from transwarp.parser.types import SectionObject

class Parser(Struct):
    def __init__(self, header, lines, comment):
        pd = RE_PARSER_DEF.match(header)
        if pd:
            self._match = pd.group(2)
            super().__init__(pd.group(1), lines, comment)
        else:
            raise ValueError("Invalid parser definition: [%r]" % header)

    @property
    def arg(self):
        return self._match
