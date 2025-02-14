r"""
    Vector operations.
"""

from numpy import ndarray, array as _array, dot
from numpy.linalg import norm, cross


def unit(v: ndarray) -> ndarray:
    return v / norm(v)


def e3(v1: ndarray, v2: ndarray) -> ndarray:
    r"""
        Get the third direction.
    """
    the_crossed = cross(v1, v2)
    norm_crossed = norm(the_crossed)
    if norm_crossed < 1e-8:
        if abs(v1[1]) < 1e-8 and abs(v1[2]) < 1e-8:
            return _array((0.0, 1.0, 0.0))
        else:
            return e3(v1, _array((1.0, 0.0, 0.0)))
    return the_crossed / norm_crossed


def cos_theta(a: ndarray, b: ndarray) -> ndarray:
    return dot(unit(a), unit(b))
