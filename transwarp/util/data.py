class SearchableList(list):

    def get(self, name, require=True):
        for x in self:
            if x.name == name:
                return x
        if require:
            raise KeyError("Could not find element with name [%r]" % (name, ))
        else:
            return None

    def without(self, *names):
        res = []
        for obj in self:
            if obj.name not in names:
                res.append(obj)
        return SearchableList(res)
