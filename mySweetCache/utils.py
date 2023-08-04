import os
from typing import Optional

import pkg_resources

from .common import SETUP


def get_package_version():
    try:
        return pkg_resources.get_distribution("mySweetCache").version
    except pkg_resources.DistributionNotFound:
        return "Unknown."


def use_par(par):
    """
    Wrapper set self argument as first function argument.
    """

    def wrap(fun):
        def INNER(*args, **kwargs):
            return fun(par, *args, **kwargs)

        INNER.__name__ = fun.__name__
        return INNER

    return wrap


def use_pars(*pars):
    """
    Wrapper set self arguments as first function arguments.
    """

    def wrap(fun):
        def INNER(*args, **kwargs):
            return fun(*pars, *args, **kwargs)

        INNER.__name__ = fun.__name__
        return INNER

    return wrap


def make_cache_dir(_CACHE_FILES: Optional[str] = None):
    _CACHE_FILES = _CACHE_FILES or SETUP.CACHE_FILES
    if _CACHE_FILES not in os.listdir():
        os.mkdir(_CACHE_FILES)
        with open(
            os.sep.join([_CACHE_FILES, ".gitignore"]), "w", encoding="utf-8"
        ) as f:
            print("# Created by mySweetCache automatically.\n*\n", file=f)
