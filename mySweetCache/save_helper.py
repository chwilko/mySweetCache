import os
from typing import Optional, Union, TypedDict, List
import json
import numpy as np

from mySweetCache.utils import get_package_version, make_cache_dir
from mySweetCache.common import SETUP

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
            "dtype": data.dtype,
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
        with open(self.store_path(SaveHelper.INFO), "w", encoding="utf-8") as f:
            json.dump(data_info, f, indent=4)
        data.tofile(self.get_data_info(file_name), sep=sep_in_data)


    def read_from_file(
        self,
        file_name: str,
        *,
        sep_in_data: str=",",
    ):
        with open(self.store_path(SaveHelper.INFO), "r", encoding="utf-8") as f:
            info: DataInfo = json.load(f)
        sep_in_data = sep_in_data or info["sep_in_data"]
        return np.fromfile(
            file_name,
            dtype=info["dtype"],
            sep=sep_in_data,
        ).reshape(info["shape"])
