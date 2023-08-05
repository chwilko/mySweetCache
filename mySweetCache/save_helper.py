import json
import os
import shutil
from typing import Optional, Tuple, TypedDict

import numpy as np

from mySweetCache.exceptions import MSCDoesNotExistException
from mySweetCache.setup import SETUP
from mySweetCache.utils import get_package_version, make_cache_dir


class DataInfo(TypedDict):
    """
    Cache data info type.
    """

    shape: Tuple[int, ...]
    dtype: str
    header: str
    version: str
    sep_in_data: str


VERSION = f"{get_package_version()}"
DEFAULT_HEADER = f"Data stored by mySweetCache{VERSION}"


def _store_path(*files) -> str:
    """Return path os.sep.join([SETUP.CACHE_FILES, *files]).
    If SETUP.CACHE_FILES not exists will be created.

    Returns:
        str: valid path in SETUP.CACHE_FILES.
    """
    if not os.path.exists(SETUP.CACHE_FILES):
        make_cache_dir()
    return os.sep.join([SETUP.CACHE_FILES, *files])


class SaveHelper:
    """
    Namespace with chache file menagnent.
    """

    INFO = "info.json"

    @classmethod
    def _create_data_info(
        cls,
        data: np.ndarray,
        header: str,
        sep_in_data: str,
    ) -> DataInfo:
        """Returned valid typed dict.

        Args:
            data (np.ndarray): data to cache
            header (str): data header.
            sep_in_data (str): Used sep in data

        Returns:
            DataInfo:  valid typed dic
        """
        info: DataInfo = {
            "shape": data.shape,
            "dtype": str(data.dtype),
            "header": header,
            "version": VERSION,
            "sep_in_data": sep_in_data,
        }
        return info

    @classmethod
    def save_to_file(
        cls,
        data: np.ndarray,
        name: str,
        *,
        header: Optional[str] = None,
        sep_in_data: str = "",
    ) -> None:
        """Method save data to cache.

        Args:
            data (np.ndarray): data to cache.
            name (str): cache key name
            header (Optional[str], optional): cache header. Defaults to None.
            sep_in_data (str, optional): Separator between array items
                for text output. If "" (empty), a binary file is written,
                equivalent to file.write(a.tobytes()). Defaults to "".
        """
        header = header or DEFAULT_HEADER
        data_info = cls._create_data_info(data, header, sep_in_data)
        cache_folder = _store_path(name)
        if not os.path.exists(cache_folder):
            os.mkdir(_store_path(name))
        with open(_store_path(name, SaveHelper.INFO), "w", encoding="utf-8") as f:
            json.dump(data_info, f, indent=4)
        data.tofile(_store_path(name, name), sep=sep_in_data)

    @classmethod
    def read_from_file(
        cls,
        name: str,
    ) -> np.ndarray:
        """Method read data from cache.

        Args:
            name (str): data to cache.

        Returns:
            np.ndarray: data readed from cache.
        """
        with open(_store_path(name, SaveHelper.INFO), "r", encoding="utf-8") as f:
            info: DataInfo = json.load(f)
        return np.fromfile(
            _store_path(name, name),
            dtype=info["dtype"],
            sep=info["sep_in_data"],
        ).reshape(info["shape"])

    @classmethod
    def cache_exists(cls, name: str) -> bool:
        """The method checks whether the cache exists

        Args:
            name (str): cache key

        Returns:
            bool: _description_
        """
        return os.path.exists(_store_path(name))

    @classmethod
    def remove_cache(cls, name: str, *, ignore_errors: bool = True) -> None:
        """Remove cache with set name.

        Args:
            name (str): Cache key name.
            ignore_errors (bool, optional): If True will not raise an error
                if the file does not exist. Defaults to True.
        """
        try:
            shutil.rmtree(_store_path(name), ignore_errors=ignore_errors)
        except FileNotFoundError as exc:
            raise MSCDoesNotExistException from exc

    @classmethod
    def remove_all_caches(cls, *, ignore_errors: bool = True) -> None:
        """Remove all caches

        Args:
            ignore_errors (bool, optional): If True will not raise an error
                if the file does not exist. Defaults to True.
        """
        shutil.rmtree(_store_path(), ignore_errors=ignore_errors)

    @classmethod
    def get_header(cls, name: str) -> str:
        """Return a cache header with the specified key.

        Args:
            name (str): Cache key name.

        Returns:
            str: Header.
        """
        with open(_store_path(name, SaveHelper.INFO), "r", encoding="utf-8") as f:
            info: DataInfo = json.load(f)
        return info["header"]

    @classmethod
    def get_cache_info(cls, name: str) -> str:
        """Return a cache header with the specified key.

        Args:
            name (str): Cache key name.

        Returns:
            str: Header.
        """
        with open(_store_path(name, SaveHelper.INFO), "r", encoding="utf-8") as f:
            info: DataInfo = json.load(f)
        return info["header"]
