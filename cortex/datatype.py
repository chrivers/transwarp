import re

class Type(object):
    def __init__(self, text):
        RE_TYPE = re.compile("(\w+)(?:<(.+)(?:, (.+))?>)?")
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, target, arg = match.groups()
        self._name = name
        self._target = Type(target)
        self._arg = arg

    @property
    def name(self):
        return self._name

class FixedArray(Type):

    def __init__(self, name, type, length):
        self._name = name
        self._type = type
        self._length = length

    @property
    def type(self):
        return self._type

    @property
    def length(self):
        return self._length

class Array(Type):

    def __init__(self, name, type, length):
        self._name = name
        self._type = type
        self._length = length

    @property
    def type(self):
        return self._type

    @property
    def length(self):
        return self._length
