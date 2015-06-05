# -*- coding: utf-8 -*-
'''

Common cache method for python. Check usage on
Example.

'''


class DontCache(Exception):
    pass


def cache(compute_key, container_factory):
    marker = object()

    def decorator(func):
        def replacement(*args, **kwargs):
            cache = container_factory()
            if cache is None:
                return func(*args, **kwargs)
            try:
                key = compute_key(*args, **kwargs)
            except DontCache:
                return func(*args, **kwargs)

            key = '{0}.{1}:{2}'.format(func.__module__,
                                       func.__name__,
                                       key)
            cached_value = cache.get(key, marker)
            if cached_value is marker:
                cached_value = cache[key] = func(*args, **kwargs)
            else:
                pass

            return cached_value

        replacement.__doc__ = func.__doc__
        return replacement

    return decorator


# Show Example
if __name__ == '__main__':
    # container is an factory function provide dict like object
    # for storing cache, the scope is limited by this factory
    def local_container():
        if 'example_cache' not in globals():
            globals()['example_cache'] = dict()

        return globals()['example_cache']

    # we always provide a more sofisticated cache function for
    # a given cache factory
    def local_cache(compute_key):
        return cache(compute_key, local_container)

    # compute_key takes exactly parameters as to be cached function
    # , it's function specified
    def _cachekey_exmample_func(selects, filters):
        key = ''
        for s in selects:
            key += s + ':'
        for f in filters:
            key += f + '-'

        return key

    # decorate the normal function is all
    @local_cache(_cachekey_exmample_func)
    def sql_query(selects, filters):
        return
