# VERY LIKELY TO BE DEPRECATED
from enum import Enum
import json


class AppText(Enum):
    """
    Enum class that contains the text to be displayed in the app
    Must call `load_text()` first.
    """

    APP_DESCRIPTION: str
    APP_DESCRIPTION_TITLE: str

    @staticmethod
    def load_text(json_file: str) -> None:
        with open(json_file, mode='r', encoding='utf-8') as text_file:
            contents: dict = json.load(text_file)
        for key in contents.keys():
            name = key.upper()
            value = contents.get(key)
            setattr(AppText, name, value)