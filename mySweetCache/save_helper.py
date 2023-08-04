import json
import os
from typing import List, Optional, TypedDict

import numpy as np

from mySweetCache.common import SETUP
from mySweetCache.utils import get_package_version, make_cache_dir


class DataInfo(TypedDict):
    shape: List[int]
    dtype: str
    header: str
    sep_in_data: str


DEFAULT_HEADER = f"Data stored by mySweetCache{get_package_version()}"


class SaveHelper:
    INFO = "info.json"

    def store_path(self, *files):
        if not os.path.exists(SETUP.CACHE_FILES):
            make_cache_dir()
        return os.sep.join([SETUP.CACHE_FILES, *files])

    def get_data_info(self, data: np.ndarray, header: str, sep_in_data: str):
        info: DataInfo = {
            "shape": data.shape,
            "dtype": str(data.dtype),
            "header": header,
            "sep_in_data": sep_in_data,
        }
        return info

    def save_to_file(
        self,
        data: np.ndarray,
        file_name: str,
        *,
        header: Optional[str] = None,
        sep_in_data: str = ",",
    ):
        header = header or DEFAULT_HEADER
        data_info = self.get_data_info(data, header, sep_in_data)
        cache_folder = self.store_path(file_name)
        if not os.path.exists(cache_folder):
            os.mkdir(self.store_path(file_name))
        with open(
            self.store_path(file_name, SaveHelper.INFO), "w", encoding="utf-8"
        ) as f:
            json.dump(data_info, f, indent=4)
        data.tofile(self.store_path(file_name, file_name), sep=sep_in_data)

    def read_from_file(
        self,
        file_name: str,
        *,
        sep_in_data: str = None,
    ):
        with open(
            self.store_path(file_name, SaveHelper.INFO), "r", encoding="utf-8"
        ) as f:
            info: DataInfo = json.load(f)
        sep_in_data = sep_in_data or info["sep_in_data"]
        return np.fromfile(
            self.store_path(file_name, file_name),
            dtype=info["dtype"],
            sep=sep_in_data,
        ).reshape(info["shape"])

    def cache_exists(self, file_name: str):
        return os.path.exists(self.store_path(file_name))
