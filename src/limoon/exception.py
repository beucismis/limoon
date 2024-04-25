from typing import Final

SHIT_MESSAGE: Final = "büyük başarısızlıklar sözkonusu"


class TopicNotFound(Exception):
    "The topic record is not available."


class EntryNotFound(Exception):
    "The entry record is not available."


class AuthorNotFound(Exception):
    "The author record is not available."


class PageNotFound(Exception):
    "The page record is not available."
