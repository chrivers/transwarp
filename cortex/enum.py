import re
from .strutil import text_width, hex_width

class Enum(object):
    def __init__(self, header, lines, comment):
        RE_ENUM_FIELD = re.compile("(\w+)\s*=\s*(\w+)")

        fields = []
        for line in lines:
            field = RE_ENUM_FIELD.match(line)
            name, value = field.groups()
            fields.append((name, int(value, 0)))
        tw = text_width(fields)
        hw = hex_width(fields)

        self._name = header
        self.fields = [Case(f[0], f[1], tw, hw) for f in fields]
        self._comment = comment

    @property
    def name(self):
        return self._name

class Flags(Enum):
    pass

class Case(object):
    def __init__(self, name, value, name_width, value_width):
        self.name = name
        self.value = value
        self._name_width = name_width
        self._value_width = value_width

    @property
    def aligned_name(self):
        return "{:{width}}".format(self.name, width=self._name_width)

    @property
    def hex_value(self):
        return "0x{:x}".format(self.value)

    @property
    def aligned_hex_value(self):
        return "0x{:0{width}x}".format(self.value, width=self._value_width)
