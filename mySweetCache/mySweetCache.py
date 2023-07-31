import os
from typing import Any, Callable, Optional

import numpy as np
from .common import SETUP
from .utils import use_par, make_cache_dir


def read_cache(MSC_name: str, cache_folder: Optional[str]=None) -> Any:
    """File to fast read MSC.

    Args:
        MSC_name (str): cache key to read.
        cache_folder (str, optional): Cache will be read from .MScache_files from cache_folder.
        If cache_folder is None is used current folder. Defaults to None.

    Raises:
        NameError: If this cache don't exist.

    Returns:
        np.array: two dimmentional matrix.
    """    
    if cache_folder is None:
        cache_folder = SETUP["CACHE_FILES"]
    cache_folder += SETUP["CACHE_FILES"]
    if not os.path.exists(os.sep.join([cache_folder, MSC_name])):
        raise NameError(f"{MSC_name} cache not exist")

    @cache(MSC_name)
    def NobodyExpectsTheSpanishInquisition():
        return
    return NobodyExpectsTheSpanishInquisition(use_cache=True)
    

def cache(MSC_name: Optional[str]=None, *, dim: int=2):
    """Wrapper add possibility caching function result to wrapped function

    Wrapper add possibility caching function result to wrapped function.
    If file MSC_name.txt exist in _CACHE_FILES
        wraped function return cache from right cache.
    else
        make new cache
    Wrapper add optional argument 'use_cache'.
    If use_cache == False
        cache will overwrite.

    Args:
        MSC_name (string, optional): name of cache (key to identify)
            If MSC_name is None then stay __name__ of cached function. Defaults to None.

    Returns:
        fun: Function with cache functionality.
    """
    if SETUP["CACHE_FILES"] not in os.listdir():
        make_cache_dir(SETUP["CACHE_FILES"])

    @use_par(MSC_name)
    def wrapper(MSC_name: Optional[str], fun: Callable):
        if MSC_name is None:
            MSC_name = fun.__name__

        def TO_RETURN(*args, use_cache: bool=SETUP["MSC_USE_CACHE"]):
            if MSC_name in os.listdir(SETUP["CACHE_FILES"]) and use_cache:
                return read_from_file(os.sep.join([SETUP["CACHE_FILES"], MSC_name]))
            ret = fun(*args)
            save_to_file(ret, os.sep.join([SETUP["CACHE_FILES"], MSC_name]), MSC_name)
            return ret

        TO_RETURN.__name__ = fun.__name__
        return TO_RETURN

    return wrapper


def save_to_file(lists, file_name, header="", sep_in_data=","):
    """The function saves the given estimated data for later use.
    To read them later, use the read_from_file function.
    Args:
        lists (_type_): A list of lists of files to save. preferably two-dimensional np.array
        file_name (string): The name of the file in which the data is to be stored.
        header (str, optional): The first line that is a description of the data,
            ignored later, when reading. Defaults to "".
        sep_in_data (str, optional): The character with which the data is to be separated. Defaults to ",".
    """
    ret = header + "\n"
    for el in lists:
        for i in el:
            ret += str(i) + sep_in_data
        ret = ret[:-1] + "\n"
    try:
        with open(file_name, "w") as f:
            f.write(ret)
    except FileNotFoundError:
        old = os.getcwd()
        path = file_name.split(os.sep)[:-1]
        for i in path:
            os.mkdir(i)
            os.chdir(i)
        os.chdir(old)
        with open(file_name, "w") as f:
            f.write(ret)


def read_from_file(file_name, sep_in_data=",", show_warr=True):
    """The function reads previously saved data with the save_to_file function.
    Args:
        file_name (string): the name of the file from which data is to be read
        sep_in_data (str, optional): The character with which the data is to be separated. Defaults to ",".
        show_warr (bool, optional): if true, the function will display a warning
            if the data cannot be converted into numbers
            and returns them as str. Defaults to True.
    Returns:
        np.array: two dimmentional matrix.
    """
    with open(file_name, "r") as f:
        data = f.read().split("\n")
    for i in range(1, len(data)):
        if data[i] == "":
            data = data[:i]
            break
        try:
            data[i] = [float(k) for k in data[i].split(sep_in_data)]
        except ValueError:
            data[i] = data[i].split(sep_in_data)
            if show_warr is False:
                continue
            print("Warring! Data was read as string.")

    return np.array(data[1:])
