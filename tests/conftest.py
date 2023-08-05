from mySweetCache.save_helper import SaveHelper


def pytest_sessionfinish(*args):  # pylint: disable=W0613
    """
    Function evaluated at the end of pytest
    """
    SaveHelper().remove_all_caches()
