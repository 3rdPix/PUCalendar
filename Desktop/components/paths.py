# VERY LIKELY TO BE DEPRECATED
import json
from enum import Enum
from os.path import join


class Paths:
    """
    Enum class with paths to important files and resources.
    Paths are constructed using os.path
    Must call `load_paths()` first.
    """
    directories: dict = {'':''}

    @staticmethod
    def get(key: str) -> str:
        return Paths.directories.get(key)

    @staticmethod
    def load_paths(json_file: str) -> None:
        with open(json_file, mode='r', encoding='utf-8') as paths_file:
            roots: dict = json.load(paths_file)
        for key in roots.keys():
            name = key
            value = join(*roots.get(key))
            Paths.directories[name] = value
