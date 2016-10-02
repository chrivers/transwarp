import os

__all__ = [
    "path_normalize",
    "path_join",
    "path_has_ext",
    "path_remove_ext",
    "path_touch",
]

def path_normalize(path):
    return os.path.normpath(path) + os.path.sep

def path_join(a, b):
    return os.path.normpath(os.path.join(a, b))

def path_has_ext(path, ext):
    return os.path.splitext(path)[1] == ext

def path_remove_ext(path, ext):
    if path_has_ext(path, ext):
        return path[:-len(ext)]
    else:
        return path

def path_touch(path):
    os.utime(path, None)
