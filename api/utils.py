from enum import Enum


class ParamOrderingSinger(Enum):
    name_asc = "name"
    name_desc = "-name"


class ParamOrderingTrack(Enum):
    name_asc = "name"
    name_desc = "-name"
    original_language_asc = "original_language"
    original_language_desc = "-original_language"
    text_asc = "text"
    text_desc = "-text"


class ParamOrderingTranslation(Enum):
    text_asc = "text"
    text_desc = "-text"
    language_asc = "language"
    language_desc = "-language"
