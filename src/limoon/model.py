import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import Callable, Iterator, TypeVar, Optional, Union

from . import constant, core


# Typings
URL = TypeError("URL", Callable, str)


@dataclass
class Entry:
    """Entry data class.

    Arguments:
    id (int): Unique entry identity.
    author_nickname (str): Author who created entry.
    content (str): Entry content (with HTML tags).
    favorite_count (int): Entry favorite count.
    date (str): Entry sting date.
    created (datetime): Datetime object of create entry.
    edited (datetime|bool): Datetime object of edit entry.
    url (str): Entry HTTP link.
    """

    id: int
    author_nickname: str
    content: str
    favorite_count: int
    date: str
    created: datetime = field(init=False)
    edited: Union[datetime, bool] = field(init=False)
    url: URL = field(init=False)

    def __repr__(self):
        return f"Entry({self.id})"

    def __post_init__(self):
        self.created, self.edited = self._parse_datetime(self.date)
        self.url = constant.BASE_URL + constant.ENTRY_ROUTE.format(self.id)

    def _parse_datetime(self, stuff: str) -> tuple[datetime, Union[datetime, bool]]:
        def parse_single(value: str) -> datetime:
            value = value.strip()

            for fmt in ("%d.%m.%Y %H:%M", "%d.%m.%Y"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

            raise ValueError(value)

        if "~" not in stuff:
            return parse_single(stuff), False

        created_str, edited_str = map(str.strip, stuff.split("~"))
        created = parse_single(created_str)

        if not edited_str:
            edited = False
        elif "." in edited_str:
            try:
                edited = datetime.strptime(edited_str, "%d.%m.%Y %H:%M")
            except ValueError:
                edited = datetime.strptime(edited_str, "%d.%m.%Y")
        else:
            edited = datetime.strptime(
                f"{created.strftime('%d.%m.%Y')} {edited_str}", "%d.%m.%Y %H:%M"
            )

        return created, edited


@dataclass
class Topic:
    """Topic data class.

    Arguments:
    id (int): Unique topic identity.
    title (str): Topic title.
    path (str): Unique topic path.
    entrys (Iterator[Entry]): Topic total entrys per page.
    page_count (int|None): Topic total page count.
    url (str): Topic HTTP link.
    """

    id: int
    title: str
    path: str
    entrys: Iterator[Entry]
    page_count: Union[int, None]
    url: URL = field(init=False)

    def __repr__(self):
        return f"Topic({self.id})"

    def __post_init__(self):
        self.url = constant.BASE_URL + constant.TOPIC_ROUTE.format(self.path)


@dataclass
class Rank:
    """Rank data class.

    Arguments:
    name (str): Custom rank name.
    karma (int): Rank karma number.
    """

    name: str
    karma: int

    def __repr__(self):
        return "Rank()"


@dataclass
class Badge:
    """Badge data class.

    Arguments:
    name (str):
    description (str):
    icon_url (str):
    """

    name: str
    description: str
    icon_url: URL

    def __repr__(self):
        return f"Badge({self.name})"


@dataclass
class Author:
    """Author data class.

    Arguments:
    nickname (str): Unique author nickname.
    biography (str|None): Author biography (with HTML tags).
    total_entry (int): Author total entry count.
    follower_count (int): Author total follower count.
    following_count (int): Author total following count.
    avatar_url (str): Author avatar HTTP link.
    rank (class): Author rank.
    badges (class): Author badges.
    url (str): Author HTTP link.
    """

    nickname: str
    biography: Union[str, None]
    total_entry: int
    follower_count: int
    following_count: int
    avatar_url: URL
    rank: Union[Rank, None] = field(init=True)
    badges: Iterator[Badge] = field(init=False)
    url: URL = field(init=False)

    def __repr__(self):
        return f"Author({self.nickname})"

    def __post_init__(self):
        self.rank = self._parse_rank(self.rank)
        self.badges = core.get_author_badges(self.nickname)
        self.url = constant.BASE_URL + constant.AUTHOR_ROUTE.format(self.nickname)

    def _parse_rank(self, stuff: Union[str, None]) -> Union[Rank, None]:
        if isinstance(stuff, type(None)):
            return None
        result = re.match(r"(\D+) \((\d+)\)", stuff.text)
        return Rank(result.group(1), int(result.group(2)))


@dataclass
class Agenda:
    """Agenda page data class.

    Arguments:
    title (str): Topic title.
    path (int): Unique topic path.
    entry_count (str): Topic total entry count.
    url (URL): Topic HTTP link.
    """

    title: str
    path: str
    entry_count: Optional[str] = None
    url: URL = field(init=False)

    def __repr__(self):
        return f"Agenda({self.title})"

    def __post_init__(self):
        self.url = constant.BASE_URL + constant.TOPIC_ROUTE.format(self.path)


@dataclass
class Debe:
    """Depe page data class.

    Arguments:
    topic_title (str): Topic title.
    id (int): Unique entry id.
    url (URL): Entry HTTP link.
    """

    topic_title: str
    id: int
    url: URL = field(init=False)

    def __repr__(self):
        return f"Debe({self.id})"

    def __post_init__(self):
        self.url = constant.BASE_URL + constant.ENTRY_ROUTE.format(self.id)


@dataclass
class SearchResult:
    """SearchResult data class.

    Arguments:
    title (str): Topic title.
    path (str): Unique topic path.
    entry_count (str|None): Topic total entry count.
    url (URL): Topic HTTP link.
    """

    title: str
    path: str
    entry_count: Optional[str] = None
    url: URL = field(init=False)

    def __repr__(self):
        return f"SearchResult({self.title})"

    def __post_init__(self):
        self.url = constant.BASE_URL + constant.TOPIC_ROUTE.format(self.path)
