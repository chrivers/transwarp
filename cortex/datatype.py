import re

class Type(object):
    def __init__(self, text):
        RE_TYPE = re.compile("(\w+)(?:<(.+)>)?")
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, args = match.groups()
        self._name = name
        self._args = {}
        if args:
            if "=" in args[0]:
                raise ValueError("First type parameter must not be key=value: [%s]" % args[0])
            self._target = args[0]

        for arg in re.split(",\s*", args or "")[1:]:
            if "=" not in arg:
                raise ValueError("All type parameters after the first must be key=value: %r (in %r)" % (arg, text))
                key, value = arg.split("=", 1)
                self.args[key.strip()] = value.strip()

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def arg(self, name, default=None):
        return self._args.get(name, default)
