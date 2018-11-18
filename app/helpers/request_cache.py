#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g
from functools import wraps

def _init():
    """
    initializes the namespace {} in the global request scope
    This way, we are able to access it anywhere we need it
    """
    g.app_cache = {}
    return

def _add(key, value):
    """
    Adds a key/value to the global app cache request {}
    """
    if not hasattr(g, 'app_cache'):
        _init()
    g.app_cache[key] = value

def _remove(key):
    """
    Removes the key from the global app cache request {}
    """
    if not hasattr(g, 'app_cache'):
        return
    g.app_cache.pop(key, None)

def _get(key):
    """
    Gets the key's value from the global app cache request {}
    """
    if not hasattr(g, 'app_cache'):
        return None
    return g.app_cache.get(key)

def destroy():
    """
    Destroys the app cache attribute
    """
    if hasattr(g, 'app_cache'):
        del g.app_cache

def _is_valid(key, func_args):
    """
    Validates that the cached value for key includes all keys and values for the provided func_args
    Protects from cache conflicts if the same function gets called with different params
    @param key str
    @param func_args {}
    @returns bool
    """
    cacheDict = _get(key) or {}
    func_arg_keys = func_args.keys()

    for arg_key in func_arg_keys:
        if cacheDict.get(arg_key) != func_args.get(arg_key):
            return False

    return True

def _add_with_func_args(key, value, func_args):
    """
    Adds a key to the cache along with the keys provided in the func_args
    This is useful for protecting against returning cached values if the
    func args are different from those in the cache
    @param key str
    @param func_args {}
    """
    # Construct a dict from the func args

    for func_arg_key in func_args.keys():
        value[func_arg_key] = func_args.get(func_arg_key)

    _add(
        key=key,
        value=value
    )

    return

def cache_func():
    """
    Caches the provided function arguments and its return value(s)
    Uses the function name and module name as the cache key
    This guarantees uniqueness of the cache key
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cacheKey = '{}.{}'.format(f.__module__, f.__name__)
            # Get the function args
            arguments = locals()

            cache_is_valid = _is_valid(
                key=cacheKey,
                func_args=arguments
            )
            print ("IS CACHE VALID for args {}? {}".format(arguments, cache_is_valid))
            if cache_is_valid:
                # Return the cached data
                return _get(cacheKey).get('return_value')

            # Get the return value of the function
            return_value = f(*args, **kwargs)

            # Cache the function args and its return value
            _add_with_func_args(
                key=cacheKey,
                value={
                    'return_value': return_value
                },
                func_args=arguments
            )

            return return_value

        return decorated_function

    return decorator