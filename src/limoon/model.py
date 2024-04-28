import re
from dataclasses import dataclass, field
from typing import Callable, Iterator, TypeVar, Union

from limoon import constant, core

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
    created (str): Datetime of create entry.
    edited (str|bool): Datetime of edit entry.
    url (str): Entry HTTP link.
    """

    id: int
    author_nickname: str
    content: str
    favorite_count: int
    created: str = field(init=True)
    edited: Union[str, bool] = field(init=False)
    url: URL = field(init=False)

    def __repr__(self):
        return f"Entry({self.id})"

    def __post_init__(self):
        self.edited = self._is_edited(self.created)
        self.url = constant.BASE_URL + constant.ENTRY_ROUTE.format(self.id)

    def _is_edited(self, stuff: str) -> Union[str, bool]:
        try:
            created, edited = stuff.split("~")
            self.created = created.strip()
        except ValueError:
            return False
        return edited.strip()


@dataclass
class Topic:
    """Topic data class.

    Arguments:
    id (int): Unique topic identity.
    title (str): Topic title.
    path (str): Unique topic path.
    entrys (class): Entrys written for topic.
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
