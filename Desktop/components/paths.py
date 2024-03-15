# VERY LIKELY TO BE DEPRECATED

from os.path import join
from enum import Enum
import json


class Paths(Enum):
    """
    Enum class with paths to important files and resources.
    Paths are constructed using os.path
    Must call `load_paths()` first.
    """

    WINDOW_ICON: str
    ABOUT_BACKGROUND: str
    TEXT: str
    QSS: str

    @staticmethod
    def load_paths(json_file: str) -> None:
        with open(json_file, mode='r', encoding='utf-8') as paths_file:
            roots: dict = json.load(paths_file)
        for key in roots.keys():
            name = key.upper()
            value = join(*roots.get(key))
            setattr(Paths, name, value)