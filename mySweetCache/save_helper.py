import os
from ast import List
from ctypes import Union
from typing import Optional

import numpy as np
from .common import DataTypes

class SaveHelper:
    def __init__(
        self,
        *,
        is_string: bool=False,
        dim: Optional[int]=2,
    ) -> None:
        if is_string:
            self.data_type = DataTypes.STRING
        else:
            self.data_type = DataTypes.NUMBER
        self.dim = dim

    def store(
        self,
        cache_name: str,
        header: str="",
    ):
        pass


    def save_to_file(
        self,
        lists: Union[np.ndarray, List[List[float]]],
        file_name: str,
        header: str = "",
        sep_in_data: str = ",",
    ):
        """The function saves the given estimated data for later use.
        To read them later, use the read_from_file function.
        Args:
            lists (Union[np.ndarray, List[List[float]]]): A list of lists of files to save. preferably two-dimensional np.array
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

    def read_from_file(
        self,
        file_name: str,
        sep_in_data: str=",",
        show_warr: bool=True,
    ):
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
                if show_warr:
                    print("Warring! Data was read as string.")

        return np.array(data[1:])
