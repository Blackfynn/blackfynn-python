import functools

try:
    import pandas
except ImportError:
    pandas = None

try:
    import numpy
except ImportError:
    numpy = None


class MissingDependency(Exception):
    pass


def require_extension(f):
    """
    Decorator that ensures the optional `data` dependencies are installed.

    All functions and methods that use `numpy` or `pandas` must be decorated
    with this.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if pandas is None or numpy is None:
            raise MissingDependency(
                """This command requires additional dependencies. To install, run:

pip install blackfynn[data]

"""
            )
        return f(*args, **kwargs)

    return wrapper
