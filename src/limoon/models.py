import re
from urllib.parse import urlparse
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Iterator, Optional, TypeVar, Union

from . import constants


# Typings
URL = TypeVar("URL", Callable, str)


@dataclass
class Entry:
    """Entry data class.

    Arguments:
    id (int): Unique entry identity.
    author_nickname (str): Author who created entry.
    text (str): Entry text.
    html (str): Entry text (with HTML tags).
    favorite_count (int): Entry favorite count.
    date (str): Entry sting date.
    topic_title (str): Entry topic title.
    topic_path (str): Unique entry topic path.
    is_pinned (bool): Entry pinned status.
    is_pinned_on_profile (bool): Entry pinned on profile status.
    images (list|None): Entry images.
    images_source (list|None): Entry images source.
    created (datetime): Datetime object of create entry.
    edited (datetime|bool): Datetime object of edit entry.
    url (str): Entry HTTP link.
    """

    id: int
    author_nickname: str
    text: str
    html: str
    favorite_count: int
    date: str
    topic_title: str
    topic_path: str
    is_pinned: bool
    is_pinned_on_profile: bool
    images: Optional[list[URL]]
    images_source: Optional[list[URL]] = field(init=False)
    created: datetime = field(init=False)
    edited: Union[datetime, bool] = field(init=False)
    url: URL = field(init=False)

    def __repr__(self):
        return f"Entry({self.id})"

    def __post_init__(self):
        self.created, self.edited = self._parse_datetime(self.date)
        self.url = constants.BASE_URL + constants.ENTRY_ROUTE.format(self.id)
        self.images_source = self._conver_image_url() if self.images else None

    def _conver_image_url(self) -> list[URL]:
        images_source = []

        for url in self.images:
            image_id = urlparse(url).path.split("/")[-1]
            source_url = constants.IMAGE_ROUTE.format(
                self.created.year,
                self.created.month,
                self.created.day,
                image_id[0],
                image_id,
            )
            images_source.append(source_url)

        return images_source

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
            edited = datetime.strptime(f"{created.strftime('%d.%m.%Y')} {edited_str}", "%d.%m.%Y %H:%M")

        return created, edited


@dataclass
class Topic:
    """Topic data class.

    Arguments:
    id (int): Unique topic identity.
    title (str): Topic title.
    path (str): Unique topic path.
    entrys (Iterator[Entry]): Topic total entrys per page.
    page_count (int): Topic total page count.
    url (str): Topic HTTP link.
    """

    id: int
    title: str
    path: str
    entrys: Iterator[Entry]
    page_count: int
    url: URL = field(init=False)

    def __repr__(self):
        return f"Topic({self.id})"

    def __post_init__(self):
        self.url = constants.BASE_URL + constants.TOPIC_ROUTE.format(self.path)


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
    biography_text (str|None): Author biography.
    biography_html (str|None): Author biography (with HTML tags).
    total_entry (int): Author total entry count.
    follower_count (int): Author total follower count.
    following_count (int): Author total following count.
    record_date (str): Author record date.
    avatar_url (str): Author avatar HTTP link.
    rank (class): Author rank.
    url (str): Author HTTP link.
    """

    nickname: str
    biography_text: Optional[str]
    biography_html: Optional[str]
    total_entry: int
    follower_count: int
    following_count: int
    record_date: str
    avatar_url: URL
    rank: Optional[Rank] = field(init=True)
    url: URL = field(init=False)

    def __repr__(self):
        return f"Author({self.nickname})"

    def __post_init__(self):
        self.rank = self._parse_rank(self.rank)
        self.url = constants.BASE_URL + constants.AUTHOR_ROUTE.format(self.nickname)

    def _parse_rank(self, stuff: Union[Rank, None]) -> Union[Rank, None]:
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
        self.url = constants.BASE_URL + constants.TOPIC_ROUTE.format(self.path)


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
        self.url = constants.BASE_URL + constants.ENTRY_ROUTE.format(self.id)


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
        self.url = constants.BASE_URL + constants.TOPIC_ROUTE.format(self.path)


@dataclass
class Channel:
    """Channel data class.

    Arguments:
    name (str): Channel name.
    description (int): Channel description.
    path (str|None): Unique channel path.
    url (URL): Channel HTTP link.
    """

    name: str
    description: str
    path: URL
    url: URL = field(init=False)

    def __repr__(self):
        return f"Channel({self.name})"

    def __post_init__(self):
        self.url = constants.BASE_URL + constants.CHANNEL_ROUTE.format(self.path)


@dataclass
class ChannelTopic:
    """ChannelTopic data class.

    Arguments:
    title (str): Topic title.
    path (int): Unique topic path.
    day (str|None): Specific entry day.
    entry_count (str): Topic total entry count.
    url (URL): Topic HTTP link.
    """

    channel_name: str
    title: str
    path: str
    day: Optional[str] = None
    entry_count: Optional[str] = None
    url: URL = field(init=False)

    def __repr__(self):
        return f"ChannelTopic({self.title})"

    def __post_init__(self):
        self.url = constants.BASE_URL + constants.TOPIC_ROUTE.format(self.path)
