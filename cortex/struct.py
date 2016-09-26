from .data import SearchableList
from .datatype import Type
from .grammar import RE_STRUCT_FIELD, RE_DOC
from .strutil import text_width
from .base import SectionObject

class Struct(SectionObject):
    def __init__(self, header, lines, comment):
        fields = []
        comment = []
        for line in lines:
            doc = RE_DOC.match(line)
            if doc:
                comment.append(doc.group(1).strip())
                continue
            field = RE_STRUCT_FIELD.match(line)
            if field:
                name, type = field.groups()
                fields.append((name, type, comment))
                comment = []
        tw = text_width(fields)
        self._name = header
        self._cmt = comment
        self._tw = tw
        self.fields = SearchableList([Field(name, Type(type), cmt) for (name, type, cmt) in fields])

    @property
    def comment(self):
        return self._cmt

    @property
    def text_width(self):
        return self._tw

class Field(SectionObject):
    def __init__(self, name, type, cmt):
        self._name = name
        self._type = type
        self._cmt = cmt

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._cmt
