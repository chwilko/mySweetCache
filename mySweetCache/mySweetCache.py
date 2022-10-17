import os

import numpy as np
from .utils import use_par, use_pars
_CACHE_FILE = ".MScache_file"
_MSC_USE_CACHE = True


def make_cache_dir(_CACHE_FILE=_CACHE_FILE):
    if _CACHE_FILE not in os.listdir():
        os.mkdir(_CACHE_FILE)


def cache(MSC_name=None):
    """Dekorator który cachuje wynik funkcji.
        Jeżeli klucz istnieje kożysta z cacha, jeżeli nie
        to zapisuje go do pliku MSC_name.
        (Jeżeli MSC_name == None zapisuje do pliku o nazwie funkcji).
        Dekorator dodaje argument opcjonalny use_cache,
            który jeżeli jest False nadpisuje cacha nowym,
            w przeciwnym wypadku kożysta z cache.
    Args:
        MSC_name (string, optional): Klucz po którym dobierany jest cache.
            If None MSC_name to nazwa cachowanej funkcji. Defaults to None.
    Returns:
        fun: funkcja która kożysta z cacha.
    """
    if _CACHE_FILE not in os.listdir():
        make_cache_dir(_CACHE_FILE)

    @use_par(MSC_name)
    def wrapper(MSC_name, fun):
        if MSC_name is None:
            MSC_name = fun.__name__

        def TO_RETURN(*args, use_cache=_MSC_USE_CACHE):
            if MSC_name in os.listdir(_CACHE_FILE) and use_cache:
                return read_from_file(os.sep.join([_CACHE_FILE, MSC_name]))
            ret = fun(*args)
            save_to_file(ret, os.sep.join([_CACHE_FILE, MSC_name]), MSC_name)
            return ret

        TO_RETURN.__name__ = fun.__name__
        return TO_RETURN

    return wrapper


def save_to_file(lists, file_name, header="", sep_in_data=","):
    """Funkcja zapisuje podane estymowane dane do późniejszego wykożystania.
    Aby je późnije odczytać należy użyć funkcji read_from_file.
    Args:
        lists (_type_): lista list plików do zapisania. najlepiej dwuwymiarowy np.array
        file_name (string): azwa pliku, w którym mają być zapisane dane
        header (str, optional): pierwsza linijka stanowiąca opis danych,
            ignorowana później, przy odczytywaniu. Defaults to "".
        sep_in_data (str, optional): znak jakim mają być oddzielane dane. Defaults to ",".
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
    """Funkcja odczytuje zapisane wczesniej dane funkcją save_to_file.
    Args:
        file_name (string): nazwa pliku, z którego mają być odczytane dane
        sep_in_data (str, optional): znak jakim mają być oddzielane dane. Defaults to ",".
        show_warr (bool, optional): jeżeli true, funkcja wyświetli ostrzerzenie
            jeżeli danych nie uda się zamienić na liczby
            i zwruci je jako str. Defaults to True.
    Returns:
        np.array: dwuwymiarowa macierz
    """
    with open(file_name, "r") as f:
        data = f.read().split("\n")
    for i in range(1, len(data)):
        if data[i] == "":
            data = data[:i]
            break
        try:
            data[i] = [float(k) for k in data[i].split(sep_in_data)]
        except:
            data[i] = data[i].split(sep_in_data)
            if show_warr is False:
                continue
            print("Warring! Dane zostały przeczytane jako str.")

    return np.array(data[1:])


if __name__ == "__main__":

    @cache("foo")
    def foo(a, b):
        return [[a + b]]

    print(foo(1, 2))
    print(foo(1, 2))
    print(foo(1, 2, use_cache=False))
    print(foo(1, 2))

    # get_name()
