from ..grammar import RE_TYPE
from . import SectionObject

class Type(SectionObject):
    def __init__(self, text):
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, argstr = match.groups()
        pargs = []
        while argstr:
            match = RE_TYPE.match(argstr)
            if match:
                a, b = match.span()
                pargs.append(Type(argstr[a:b]))
                argstr = argstr[b:].strip()
                if argstr.startswith(","):
                    argstr = argstr[1:].lstrip()
            else:
                raise ValueError("Could not parse type argument [%r]" % argstr)
                break

        self._name = name
        self._args = pargs

    def arg(self, idx):
        if idx < len(self._args):
            return self._args[idx]

    def ref(self, arg):
        return "[%s as %s]" % (self.name, arg)
