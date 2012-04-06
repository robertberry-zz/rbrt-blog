"""General utils file.
"""

from functools import wraps
from flask import g, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

class memoized(object):
    """Decorator for memoizing functions.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        """On invoking try returning cached version: otherwise, call
        function and return result.
        """
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # not able to cache - one of the arguments must be either
            # mutable or non-hashable. skip caching
            return self.func(*args)

    def __repr__(self):
        """Return the functions docstring.
        """
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods.
        """
        return functools.partial(self.__call__, obj)
