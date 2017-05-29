def filterfunc(filters):

    def ffunc(name):
        for path in filters:
            if name.startswith(path):
                return True
        return False

    if filters:
        return ffunc
    else:
        return lambda _: True
