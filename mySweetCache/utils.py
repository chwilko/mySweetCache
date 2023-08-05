import os

import pkg_resources

from .setup import SETUP


def get_package_version() -> str:
    """Get package version. If unknown 'Unknown'

    Returns:
        str: package version.
    """
    try:
        return pkg_resources.get_distribution("mySweetCache").version
    except pkg_resources.DistributionNotFound:
        return "Unknown."


def use_par(par):
    """
    Decorator set self argument as first function argument.
    """

    def wrap(fun):
        def INNER(*args, **kwargs):
            return fun(par, *args, **kwargs)

        INNER.__name__ = fun.__name__
        return INNER

    return wrap


def use_pars(*pars):
    """
    Decorator set self arguments as first function arguments.
    """

    def wrap(fun):
        def INNER(*args, **kwargs):
            return fun(*pars, *args, **kwargs)

        INNER.__name__ = fun.__name__
        return INNER

    return wrap


def make_cache_dir():
    """Create cache folder"""
    _CACHE_FILES = SETUP.CACHE_FILES
    if _CACHE_FILES not in os.listdir():
        os.mkdir(_CACHE_FILES)
        val = ""
        if SETUP.IGNORE_CACHES:
            val = "*"
        with open(
            os.sep.join([_CACHE_FILES, ".gitignore"]), "w", encoding="utf-8"
        ) as f:
            print(f"# Created by mySweetCache automatically.\n\n{val}", file=f)
