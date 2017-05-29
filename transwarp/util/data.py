class SearchableList(list):

    def __contains__(self, name):
        for x in self:
            if x.name == name:
                return True
        return False

    def get(self, name, default=...):
        for x in self:
            if x.name == name:
                return x
        if default == ...:
            raise KeyError("Could not find element with name [%r]" % (name, ))
        else:
            return default

    def without(self, *names):
        res = []
        for obj in self:
            if obj.name not in names:
                res.append(obj)
        return SearchableList(res)
