import re
from dataclasses import dataclass, field
from typing import Iterator, Union

from limoon import constant

# Typings
_URL = str


@dataclass
class Rank:
    name: str
    karma: int

    def __repr__(self):
        return "Rank()"


@dataclass
class Entry:
    id: int
    author_nickname: str
    content: str
    favorite_count: int
    created: str = field(init=True)
    edited: Union[str, bool] = field(init=False)
    url: _URL = field(init=False)

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
    id: int
    title: str
    path: str
    entrys: Iterator[Entry]
    page_count: int
    url: _URL = field(init=False)

    def __repr__(self):
        return f"Topic({self.id})"

    def __post_init__(self):
        self.url = constant.BASE_URL + constant.TOPIC_ROUTE.format(self.path)


@dataclass
class Author:
    nickname: str
    biography: Union[str, None]
    total_entry: int
    follower_count: int
    following_count: int
    avatar_url: _URL
    rank: Union[Rank, None] = field(init=True)
    url: _URL = field(init=False)

    def __repr__(self):
        return f"Author({self.nickname})"

    def __post_init__(self):
        self.rank = self._parse_rank(self.rank)
        self.url = constant.BASE_URL + constant.AUTHOR_ROUTE.format(self.nickname)

    def _parse_rank(self, stuff: Union[str, None]) -> Union[Rank, None]:
        if isinstance(stuff, type(None)):
            return None
        result = re.match(r"(\D+) \((\d+)\)", stuff.text)
        return Rank(result.group(1), int(result.group(2)))
