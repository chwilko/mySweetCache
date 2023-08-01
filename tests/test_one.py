import numpy as np
from mySweetCache import cache, use_par

def test_one():
    name = "test_one"
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