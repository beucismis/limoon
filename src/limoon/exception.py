from typing import Final


SHIT_MESSAGE: Final = "büyük başarısızlıklar sözkonusu"
SEARCH_SHIT_MESSAGE: Final = "yok bişii pek"


class TopicNotFound(Exception):
    """The topic record is not available."""


class EntryNotFound(Exception):
    """The entry record is not available."""


class AuthorNotFound(Exception):
    """The author record is not available."""


class PageNotFound(Exception):
    """The page record is not available."""


class SearchResultNotFound(Exception):
    """Raised when no search results are found."""
