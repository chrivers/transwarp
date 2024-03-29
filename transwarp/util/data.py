class SearchableList(object):

    def __init__(self, elms=None):
        self.data = elms or []

    def __bool__(self):
        return len(list(self)) > 0

    def __contains__(self, name):
        for x in self.data:
            if x.name == name:
                return True
        return False

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __iter__(self):
        for elm in self.data:
            if not elm.name.startswith("@"):
                yield elm

    def __str__(self):
        return "[%s]" % (", ".join("{%s}" % (elm.name) for elm in self.data))

    def __repr__(self):
        return "[%s]" % (", ".join(repr(elm) for elm in self.data))

    def all(self):
        return iter(self.data)

    def append(self, val):
        self.data.append(val)

    def sort(self):
        self.data.sort()

    def get(self, name, default=...):
        for x in self.data:
            if x.name == name:
                return x
        if default == ...:
            raise KeyError("Could not find element with name [%r]" % (name, ))
        else:
            return default

    def without(self, *names):
        for obj in self:
            if obj.name not in names:
                yield obj
