class SectionObject(object):

    def __repr__(self):
        return "%s<%s>" % (self.__class__.__name__, self.name)

    @property
    def name(self):
        return self._name
