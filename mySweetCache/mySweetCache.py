import os
from typing import Any, Callable, Optional

from numpy import ndarray

from mySweetCache.exceptions import MSCDoesNotExistException

from .common import SETUP
from .save_helper import SaveHelper
from .utils import make_cache_dir, use_par


def read_cache(MSC_name: str, cache_folder: Optional[str] = None) -> Any:
    # """Function to fast read MSC.

    # Args:
    #     MSC_name (str): cache key to read.
    #     cache_folder (str, optional): Cache will be read from cache_folder if None
    #         .MScache_files. Defaults None.
    #     If cache_folder is None is used current folder. Defaults to None.

    # Raises:
    #     NameError: If this cache don't exist.

    # Returns:
    #     np.array: two dimmentional matrix.
    # """
    if cache_folder is None:
        cache_folder = SETUP.CACHE_FILES
    print(os.sep.join([cache_folder, MSC_name]))
    if not os.path.exists(os.sep.join([cache_folder, MSC_name])):
        raise MSCDoesNotExistException(f"{MSC_name} cache not exist")

    @cache(MSC_name)
    def NobodyExpectsTheSpanishInquisition():
        return

    return NobodyExpectsTheSpanishInquisition(use_cache=True)


def cache(
    MSC_name: Optional[str] = None,
    *,
    header: Optional[str] = None,
    sep_in_data: str = ",",
):
    # """Wrapper add possibility caching function result to wrapped function

    # Wrapper add possibility caching function result to wrapped function.
    # If file MSC_name.txt exist in _CACHE_FILES
    #     wraped function return cache from right cache.
    # else
    #     make new cache
    # Wrapper add optional argument 'use_cache'.
    # If use_cache == False
    #     cache will overwrite.

    # Args:
    #     MSC_name (string, optional): name of cache (key to identify)
    #         If MSC_name is None then stay __name__ of cached function. Defaults to None.

    # Returns:
    #     fun: Function with cache functionality.
    # """
    if SETUP.CACHE_FILES not in os.listdir():
        make_cache_dir(SETUP.CACHE_FILES)

    @use_par(MSC_name)
    def wrapper(MSC_name: Optional[str], fun: Callable[[], ndarray]):
        MSC_name = MSC_name or fun.__name__

        def TO_RETURN(*args, use_cache: Optional[bool] = None):
            if use_cache is None:
                use_cache = SETUP.MSC_USE_CACHE
            save_helper = SaveHelper()
            if save_helper.cache_exists(MSC_name) and use_cache:
                return save_helper.read_from_file(
                    MSC_name,
                    sep_in_data=sep_in_data,
                )
            ret = fun(*args)
            save_helper.save_to_file(
                ret,
                MSC_name,
                header=header,
                sep_in_data=sep_in_data,
            )
            return ret

        TO_RETURN.__name__ = fun.__name__
        return TO_RETURN

    return wrapper
