from builtins import object

from blackfynn.models import _get_all_class_args


def test_get_all_class_args():
    class A(object):
        def __init__(self, x, y, **kwargs):
            pass

    class B(A):
        def __init__(self, y, z, *args):
            pass

    assert _get_all_class_args(B) == set(["self", "x", "y", "z", "args", "kwargs"])
