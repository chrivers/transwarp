from .grammar import RE_TYPE

class Type(object):
    def __init__(self, text):
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, arg0, arg1 = match.groups()
        self._name = name
        if name == "map":
            self._arg    = arg0
            self._target = Type(arg1)
        elif name in ("enum8", "enum32", "array", "option"):
            self._target = Type(arg0)
            self._arg = arg1
        elif name == "sizedarray":
            self._target = Type(arg0)
            self._arg = int(arg1)
        else:
            self._arg = arg0
            self._target = None

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def arg(self):
        return self._arg
