from transwarp.util.data import SearchableList
from ..grammar import RE_ENUM_FIELD
from ..strutil import text_width, hex_width
from . import SectionObject

class Enum(SectionObject):
    def __init__(self, header, lines, comment):
        fields = []
        for line in lines:
            field = RE_ENUM_FIELD.match(line)
            name, value = field.groups()
            fields.append((name, int(value, 0)))
        tw = text_width(fields)
        hw = hex_width(fields)

        self._name = header
        self.fields = SearchableList([Case(f[0], f[1], tw, hw) for f in fields])
        self._comment = comment

class Flags(Enum):
    pass

class Case(SectionObject):
    def __init__(self, name, value, name_width, value_width):
        self._name = name
        self._value = value
        self._name_width = name_width
        self._value_width = value_width

    @property
    def aligned_name(self):
        return "{:{width}}".format(self.name, width=self._name_width)

    @property
    def hex_value(self):
        return "0x{:x}".format(self._value)

    @property
    def aligned_hex_value(self):
        return "0x{:0{width}x}".format(self._value, width=self._value_width)
