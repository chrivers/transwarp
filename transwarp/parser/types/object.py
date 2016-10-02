from transwarp.util.data import SearchableList
from ..grammar import RE_PARSER_DEF, RE_STRUCT_FIELD, RE_DOC
from ..strutil import text_width
from .datatype import Type
from .struct import Struct
from . import SectionObject

class Object(Struct):
    def __init__(self, header, lines, comment):
        pd = RE_PARSER_DEF.match(header)
        if pd:
            self._match = pd.group(2)
            super().__init__(pd.group(1), lines, comment)
        else:
            raise ValueError("Invalid object definition: [%r]" % header)

    @property
    def arg(self):
        return self._match
