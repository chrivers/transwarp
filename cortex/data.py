class SearchableList(list):

    def get(self, name):
        for x in self:
            if x.name == name:
                return x
