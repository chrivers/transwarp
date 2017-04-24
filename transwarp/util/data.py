class SearchableList(list):

    def get(self, name):
        for x in self:
            if x.name == name:
                return x
        raise KeyError("Could not find element with name [%r]" % (name, ))
