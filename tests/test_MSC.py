import inspect
import numpy as np
import pytest
from mySweetCache import cache, use_par, read_cache
from mySweetCache.utils import use_pars

def get_random_matrix_str(low, high, size):
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


def typical_test(name, size, gen, dtype=None):
    if dtype:
        expected = gen(size=size, dtype=dtype)
    else:
        expected = gen(size=size)
    print(expected.dtype)
    @cache(name)
    def foo():
        return expected
    
    actual1 = foo(use_cache=False)
    actual2 = read_cache(name)
    assert np.all(expected == actual1)
    assert expected.dtype == actual1.dtype
    assert np.all(expected == actual2)
    assert expected.dtype == actual2.dtype

def test_other_function_same_key():
    name = inspect.currentframe().f_code.co_name
    a = np.random.random((4,5))
    b = np.random.random((4,6))
    @cache(name)
    @use_par(a)
    def identical(x):
        return x
    @cache(name)
    @use_par(a)
    def get_other(x):
        return b
    b = identical(use_cache = False)
    c = get_other()
    assert np.all(c==a)
    assert np.all(b==a)

def test_read_cache():    
    name = inspect.currentframe().f_code.co_name
    expected = np.random.random((4,5))
    @cache(name)
    @use_par(expected)
    def identical(x):
        return x
    
    identical(use_cache = False)

    actual = read_cache(name)
    print(actual)
    print(expected)
    assert np.all(actual == expected)


@pytest.mark.parametrize(
    "size",
        (
            (10,),
            (2,2),
            (2,2,2),
            (2,2,2,2),
            (2,2,2,2),
            (4,2,1,4,2),
        )
)
def test_different_dims_float(size: tuple):
    name = inspect.currentframe().f_code.co_name
    typical_test(name,size, np.random.random)


@pytest.mark.parametrize(
    "size",
        (
            (10,),
            (2,2),
            (2,2,2),
            (2,2,2,2),
            (2,2,2,2),
            (4,2,1,4,2),
        )
)
def test_different_dims_uint(size: tuple):
    name = inspect.currentframe().f_code.co_name
    @use_pars(0, 2**16-1)
    def gen(low, high, size, dtype):
        return np.random.randint(low, high, size=size, dtype=dtype)

    typical_test(name,size, gen, "uint16")

    

@pytest.mark.parametrize(
    "size",
        (
            (10,),
            (2,2),
            (2,2,2),
            (2,2,2,2),
            (2,2,2,2),
            (4,2,1,4,2),
        )
)
def test_different_dims_int(size: tuple):
    name = inspect.currentframe().f_code.co_name
    @use_pars(-(2**15-1), 2**15-1)
    def gen(low, high, size, dtype):
        return np.random.randint(low, high, size=size, dtype=dtype)

    typical_test(name,size, gen, "int16")

@pytest.mark.parametrize(
    "size",
        (
            (10,),
            (2,2),
            (2,2,2),
            (2,2,2,2),
            (2,2,2,2),
            (4,2,1,4,2),
        )
)
def test_different_dims_str(size: tuple):
    name = inspect.currentframe().f_code.co_name
    @use_pars(4, 5)
    def gen(low, high, size):
        return get_random_matrix_str(low, high, size=size)

    typical_test(name,size, gen)

