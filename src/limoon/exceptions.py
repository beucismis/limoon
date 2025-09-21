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


class ChannelNotFound(Exception):
    """The channel name is not available."""


class HTMLParsingError(Exception):
    """Raised when an error occurs while parsing HTML."""


class ElementNotFound(HTMLParsingError):
    """Raised when a required HTML element is not found."""

    def __init__(self, message: str, html: str):
        self.message = message
        self.html = html
        super().__init__(self.message)
