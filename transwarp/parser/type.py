from transwarp.parser.grammar import RE_TYPE

class Type(object):

    @classmethod
    def parse(cls, text):
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, argstr = match.groups()
        pargs = []
        while argstr:
            match = RE_TYPE.match(argstr)
            if match:
                a, b = match.span()
                pargs.append(cls.parse(argstr[a:b]))
                argstr = argstr[b:].strip()
                if argstr.startswith(","):
                    argstr = argstr[1:].lstrip()
            else:
                raise ValueError("Could not parse type argument [%r]" % argstr)
                break
        return cls(name, pargs)

    def __init__(self, name, args, link=None):
        self._name = name
        self._args = args
        self._link = link

    def __getitem__(self, index):
        if index < len(self._args):
            return self._args[index]

    def __len__(self):
        return len(self._args)

    def __repr__(self):
        arg = "{%s}" % self._link.fullname if self._link else ""
        if len(self._args):
            return "%s%s <%s>" % (self.name, arg, ",  ".join(repr(e) for e in self._args))
        else:
            return "%s%s" % (self.name, arg)

    @property
    def name(self):
        return self._name

    @property
    def link(self):
        return self._link
