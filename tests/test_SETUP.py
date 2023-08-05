# pylint: disable=E1120
import inspect

import numpy as np

from mySweetCache import SETUP, cache
from mySweetCache.save_helper import SaveHelper


def test_auto_use_cache_true():
    """
    test SETUP.MSC_USE_CACHE
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore
    initial_val = SETUP.MSC_USE_CACHE
    try:
        SETUP.MSC_USE_CACHE = True

        @cache(name)
        def testing_fun():
            return np.random.random(size=(1,))

        val0 = testing_fun()
        val1 = testing_fun()
        val2 = testing_fun(use_cache=False)
        assert val0 == val1
        assert val0 != val2
    finally:
        SETUP.MSC_USE_CACHE = initial_val


def test_auto_use_cache_false():
    """
    test SETUP.MSC_USE_CACHE
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore
    initial_val = SETUP.MSC_USE_CACHE
    try:
        SETUP.MSC_USE_CACHE = False

        @cache(name)
        def testing_fun():
            return np.random.random(size=(1,))

        val0 = testing_fun()
        val1 = testing_fun(use_cache=True)
        val2 = testing_fun()
        assert val0 == val1
        assert val0 != val2
    finally:
        SETUP.MSC_USE_CACHE = initial_val


def test_use_other_cache_folder_names():
    """
    test SETUP.CACHE_FILES (name of cache file)
    """
    name = inspect.currentframe().f_code.co_name  # type: ignore
    initial_name = SETUP.CACHE_FILES
    try:

        @cache(name)
        def testing_fun():
            return np.random.random(size=(1,))

        val0 = testing_fun()
        val1 = testing_fun()
        assert val0 == val1
        SETUP.CACHE_FILES = ".mscache"
        val2 = testing_fun()
        assert val0 != val2
    finally:
        SaveHelper().remove_all_caches()
        SETUP.CACHE_FILES = initial_name
