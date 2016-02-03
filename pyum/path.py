import os

__author__ = 'drews'

def expand(path):
    return os.path.abspath(os.path.expanduser(path))