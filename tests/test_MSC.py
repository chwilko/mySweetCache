# pylint: disable=E1120
import inspect
from typing import Callable, Optional, Tuple, Union

import numpy as np
import pytest

from mySweetCache import cache, read_cache, save_cache, use_par, use_pars


def get_random_matrix_str(
    low: int,
    high: int,
    size: Tuple[int, ...],
) -> np.ndarray:
    """Function return random matrix with str value.

    Args:
        low (int): low size of str length (include).
        high (int): high size of str length (exclude).
        size (Tuple[int, ...]): matrix size.

    Returns:
        np.ndarray: Function return random matrix with str value.
    """
    N = 1
    for val in size:
        N *= val
    strings = []
    for _ in range(N):
        string = ""
        for _ in range(np.random.randint(low, high)):
            string += chr(np.random.randint(65, 91))
        strings.append(string)
    return np.array([strings], dtype="str").reshape(size)


def typical_cache_test(
    name: str,
    size: Tuple[int, ...],
    gen: Callable,
    dtype: Union[str, Optional[np.dtype]] = None,
):
    """Typical test cache function.
    This test check how value is saved. It will be used fo other matrix types.

    Args:
        name (str): cache key name
        size (Tuple[int, ...]): matrix size
        gen (Callable): function generate random matrix with set dtype.
        dtype (Union[str, Optional[np.dtype]], optional): dtype used in gen.
            Defaults to None.
    """
    if dtype:
        expected = gen(size=size, dtype=dtype)
    else:
        expected = gen(size=size)

    @cache(name)
    def testing_fun():
        return expected

    actual1 = testing_fun(use_cache=False)
    actual2 = read_cache(name)
    assert np.all(expected == actual1)
    assert expected.dtype == actual1.dtype
    assert np.all(expected == actual2)
    assert expected.dtype == actual2.dtype


def test_use_no_nparray_output():
    """
    Test verifies that you can use the cache not only for class np.array,
    but also for a list of the right size.
    """    
    name: str = inspect.currentframe().f_code.co_name  # type: ignore
    expected = [[1,2], [0.3,0.45]]
    @cache(name)
    def testing_fun():
        return expected
    
    actual = testing_fun(use_cache=False)
    assert np.all(np.array(expected) == actual)


def typical_save_test(
    name: str,
    size: Tuple[int, ...],
    gen: Callable,
    dtype: Union[str, Optional[np.dtype]] = None,
):
    """Typical test save function.
    This test check how value is saved. It will be used fo other matrix types.

    Args:
        name (str): cache key name
        size (Tuple[int, ...]): matrix size
        gen (Callable): function generate random matrix with set dtype.
        dtype (Union[str, Optional[np.dtype]], optional): dtype used in gen.
            Defaults to None.
    """
    if dtype:
        expected = gen(size=size, dtype=dtype)
    else:
        expected = gen(size=size)

    save_cache(name, expected)
    actual1 = read_cache(name)
    assert np.all(expected == actual1)
    assert expected.dtype == actual1.dtype


def test_other_function_same_key():
    """Function check shared one cache file for two functions with one cache key."""
    name: str = inspect.currentframe().f_code.co_name  # type: ignore
    a = np.random.random((4, 5))
    b = np.random.random((4, 6))

    @cache(name)
    @use_par(a)
    def identical(arg1):
        return arg1

    @cache(name)
    @use_par(a)
    def get_other(arg1):  # pylint: disable=W0613
        return b

    b = identical(use_cache=False)
    c = get_other()
    assert np.all(c == a)
    assert np.all(b == a)


@pytest.mark.parametrize(
    "size",
    (
        (1,),
        (10,),
        (2, 2),
        (2, 2, 2),
        (2, 2, 2, 2),
        (2, 2, 2, 2),
        (4, 2, 1, 4, 2),
    ),
)
def test_different_dims_float(size: tuple):
    """Function test cache for float dtype

    Args:
        size (tuple): set matrix shape
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore
    typical_cache_test(name, size, np.random.random)
    typical_save_test(name, size, np.random.random)


@pytest.mark.parametrize(
    "size",
    (
        (10,),
        (2, 2),
        (2, 2, 2),
        (2, 2, 2, 2),
        (2, 2, 2, 2),
        (4, 2, 1, 4, 2),
    ),
)
def test_different_dims_uint(size: tuple):
    """Function test cache for uint dtype

    Args:
        size (tuple): set matrix shape
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore

    @use_pars(0, 2**16 - 1)
    def gen(low, high, size, dtype):
        return np.random.randint(low, high, size=size, dtype=dtype)

    typical_cache_test(name, size, gen, "uint16")
    typical_save_test(name, size, gen, "uint16")


@pytest.mark.parametrize(
    "size",
    (
        (10,),
        (2, 2),
        (2, 2, 2),
        (2, 2, 2, 2),
        (2, 2, 2, 2),
        (4, 2, 1, 4, 2),
    ),
)
def test_different_dims_int(size: tuple):
    """Function test cache for int dtype

    Args:
        size (tuple): set matrix shape
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore

    @use_pars(-(2**15 - 1), 2**15 - 1)
    def gen(low, high, size, dtype):
        return np.random.randint(low, high, size=size, dtype=dtype)

    typical_cache_test(name, size, gen, "int16")
    typical_save_test(name, size, gen, "int16")


@pytest.mark.parametrize(
    "size",
    (
        (10,),
        (2, 2),
        (2, 2, 2),
        (2, 2, 2, 2),
        (2, 2, 2, 2),
        (4, 2, 1, 4, 2),
    ),
)
def test_different_dims_str(size: tuple):
    """Function test cache for char dtype

    Args:
        size (tuple): set matrix shape
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore

    @use_pars(0, 8)
    def gen(low, high, size):
        return get_random_matrix_str(low, high, size=size)

    typical_cache_test(name, size, gen)
    typical_save_test(name, size, gen)
