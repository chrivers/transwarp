import re

class Type(object):
    def __init__(self, text):
        RE_TYPE = re.compile("(\w+)(?:<(.+)>)?")
        match = RE_TYPE.match(text)
        if not match:
            raise ValueError("Could not parse type [%r]" % text)
        name, args = match.groups()
        self._name = name
        self._args = args
    
    @property
    def name(self):
        return self._name
    
    @property
    def args(self):
        return self._args
