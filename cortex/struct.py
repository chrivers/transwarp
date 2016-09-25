import re
from .data import SearchableList
from .datatype import Type
from .grammar import *

class Struct(object):
    def __init__(self, header, lines, comment):
        RE_STRUCT_FIELD = re.compile("(\w+):\s*(.*)")
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

    @property
    def name(self):
        return self._name

class Field(object):
    def __init__(self, name, datatype, cmt):
        self._name = name
        self._type = datatype
        self._cmt = cmt

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._cmt
