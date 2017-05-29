import os
import datetime

__all__ = [
    "path_normalize",
    "path_join",
    "path_has_ext",
    "path_remove_ext",
    "path_touch",
    "path_mtime",
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
    try:
        os.utime(path, None)
        return True
    except FileNotFoundError:
        return False

def path_mtime(target=None):
    try:
        return datetime.datetime.fromtimestamp(os.stat(target).st_mtime)
    except IOError:
        return None
