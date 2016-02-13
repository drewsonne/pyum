import hashlib
import os
import pickle
import inspect
from pyum.path import expand

__author__ = 'drews'

lifetime = 3600
cache_keys = None
default_cache_path = '~/.yum2s3/cache/'


def __init__(self, function, function_arg_name):
    self.f = function
    self.arg_names = function_arg_name


def __call__(self, *args, **kwargs):
    if args:
        arg_names = self.arg_names
        if 'self' in arg_names:
            arg_names.remove('self')
        key_args = dict(zip(arg_names, args))
        key_args.update(kwargs)
    else:
        key_args = kwargs
    self._initialise(cache_path=expand(self.cache_path))
    key = self._build_key(key_args)
    if self.key_exists(key):
        result = self.get_key(key)
    else:
        result = self.f()
        self.set_key(key, result)
    return result


def _build_key(function_name, key_elements, args):
    m = hashlib.sha512()
    m.update(function_name.encode('utf-8'))
    for key in key_elements:
        if key in args:
            m.update(args[key].encode('utf-8'))
    return m.hexdigest()


def _initialise(cache_path):
    cache_path = expand(cache_path)

    def initialise_path(path):
        if not os.path.isdir(path):
            (head, tail) = os.path.split(path)
            if not os.path.isdir(head):
                initialise_path(head)
            os.mkdir(path)

    initialise_path(cache_path)


def _key_exists(key, cache_path):
    return os.path.exists(_key_path(key, cache_path))


def _key_path(key, cache_path):
    return os.path.join(expand(cache_path), key)


def _store_key(key, cache_path, result):
    path = _key_path(key, cache_path)

    with open(path, 'wb+') as fp:
        pickle.dump(result, fp)


def _get_cache(key, cache_path):
    path = _key_path(key, cache_path)

    with open(path, 'rb') as fp:
        return pickle.load(fp)


def opts(*opts_args, **opts_kwargs):
    def wrapper(func):
        def decorator(self, *args, **kwargs):
            func_arg_names = inspect.getargspec(func)[0]
            if 'self' in func_arg_names:
                func_arg_names.remove('self')
            # Initiailise cache path
            if 'cache_path' in opts_kwargs:
                cache_path = opts_kwargs['cache_path']
            else:
                cache_path = default_cache_path
            _initialise(cache_path)

            key = _build_key(func.__name__, opts_kwargs['keys'], dict(zip(func_arg_names, args)))

            if _key_exists(key, cache_path):
                result = _get_cache(key, cache_path)
            else:
                result = func(self, *args, **kwargs)
                _store_key(key, cache_path, result)
            return result

        return decorator

    return wrapper
