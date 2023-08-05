import os
from typing import Any, Callable, Optional

from numpy import ndarray

from mySweetCache.exceptions import MSCDoesNotExistException
from mySweetCache.save_helper import SaveHelper
from mySweetCache.setup import SETUP
from mySweetCache.utils import make_cache_dir, use_par


def read_cache(MSC_name: str) -> Any:
    """Function to fast read MSC.

    Args:
        MSC_name (str): cache key to read.

    Raises:
        NameError: If this cache don't exist.

    Returns:
        np.array: Previously saved data.
    """
    cache_folder = SETUP.CACHE_FILES
    if not os.path.exists(os.sep.join([cache_folder, MSC_name])):
        raise MSCDoesNotExistException(f"{MSC_name} cache not exist")

    return SaveHelper.read_from_file(MSC_name)


def save_cache(
    MSC_name: str,
    data: ndarray,
    *,
    header: Optional[str] = None,
    sep_in_data: str = "",
) -> None:
    """Function to fast save MSC.

    Args:
        MSC_name (str): cache key to save.
        data (ndarray): data to save
        sep_in_data (Optional[str], optional): Separator between array items
            for text output. If "" (empty), a binary file is written,
            equivalent to file.write(a.tobytes()).
    """

    SaveHelper.save_to_file(data, MSC_name, header=header, sep_in_data=sep_in_data)


def cache(
    MSC_name: Optional[str] = None,
    *,
    header: Optional[str] = None,
    sep_in_data: str = "",
) -> Callable:
    """Wrapper add possibility caching function result to wrapped function

    If file MSC_name exist in _CACHE_FILES
        wraped function return cache from right cache.
    else
        make new cache
    Wrapper add optional argument 'use_cache'.
    If use_cache == False
        cache will overwrite.

    example use:
        @cache("key")
        def long_working_function() -> np.ndarray:
            # long code to work
            return ...

    example use 2:
        @cache("key")
        @use_parms(11, 21)
        def long_working_function(arg1, arg2) -> np.ndarray:
            # long code to work
            return ...


    Args:
        MSC_name (Optional[str], optional): cache key. Defaults to None.
        header (Optional[str], optional): data description. Defaults to None.
        sep_in_data (str, optional): Separator between array items
            for text output. If "" (empty), a binary file is written,
            equivalent to file.write(a.tobytes()). Defaults to "".

    Returns:
        callable: Function with cache functionality.
    """
    if SETUP.CACHE_FILES not in os.listdir():
        make_cache_dir()

    @use_par(MSC_name)
    def wrapper(
        MSC_name: Optional[str],
        fun: Callable[[], ndarray],
    ):
        MSC_name = MSC_name or fun.__name__

        def TO_RETURN(*args, use_cache: Optional[bool] = None):
            if use_cache is None:
                use_cache = SETUP.MSC_USE_CACHE
            # SaveHelper = SaveHelper()
            if SaveHelper.cache_exists(MSC_name) and use_cache:
                return SaveHelper.read_from_file(
                    MSC_name,
                )
            ret = fun(*args)
            SaveHelper.save_to_file(
                ret,
                MSC_name,
                header=header,
                sep_in_data=sep_in_data,
            )
            return ret

        TO_RETURN.__name__ = fun.__name__
        return TO_RETURN

    return wrapper
