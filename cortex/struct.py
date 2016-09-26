from .data import SearchableList
from .datatype import Type
from .grammar import RE_STRUCT_FIELD, RE_DOC
from .base import SectionObject

class Struct(SectionObject):
    def __init__(self, header, lines, comment):
        fields = SearchableList()
        comment = []
        for line in lines:
            doc = RE_DOC.match(line)
            if doc:
                comment.append(doc.group(1).strip())
                continue
            field = RE_STRUCT_FIELD.match(line)
            if field:
                name, datatype = field.groups()
                fields.append(Field(name, Type(datatype), comment))
                comment = []
        self._name = header
        self._comment = comment
        self.fields = fields

class Field(SectionObject):
    def __init__(self, name, datatype, cmt):
        self._name = name
        self._type = datatype
        self._cmt = cmt

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._cmt
