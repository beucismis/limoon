from http import HTTPStatus
from typing import Callable, Iterator, TypeVar, Union
from urllib.parse import urlparse

from requests_html import HTMLResponse, HTMLSession

from limoon import constant, exception, model, utils

# Typings
EntryID = TypeVar("EntryID", Callable, int)
TopicKeywords = TypeVar("TopicKeywords", Callable, str)
Nickname = TypeVar("Nickname", Callable, str)
SearchKeywords = TypeVar("SearchKeywords", Callable, str)

# Session
session = HTMLSession()


def request(endpoint: str, params: dict = {}) -> HTMLResponse:
    return session.get(constant.BASE_URL + endpoint, params=params)


def get_topic(
    topic_keywords: TopicKeywords, max_entry: int = None, page: int = 1
) -> model.Topic:
    """This function get Ekşi Sözlük topic.

    Arguments:
    topic_keywords (str): Keywords (or path) of topic to be get.
    max_entry (int=None): Maximum number of entrys get from per page.
    page (int=1): Specific topic page.

    Returns:
    model.Topic (class): Topic data class.
    """

    if not isinstance(page, int):
        raise TypeError

    r = request(constant.TOPIC_ROUTE.format(topic_keywords), params={"p": page})

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exception.TopicNotFound()

    h1 = r.html.find("h1#title", first=True)
    path = h1.find("a", first=True).attrs["href"]
    page_count = r.html.find("div.pager", first=True)

    return model.Topic(
        int(h1.attrs["data-id"]),
        h1.attrs["data-title"],
        path[1:],
        utils.entry_parser(r.html, max_entry),
        int(page_count.attrs["data-pagecount"]) if page_count else page_count,
    )


def get_entry(entry_id: EntryID) -> model.Entry:
    """This function get Ekşi Sözlük entry.

    Arguments:
    entry_id (int): Unique entry identity.

    Returns:
    model.Entry (class): Entry data class.
    """

    if not isinstance(entry_id, int):
        raise TypeError

    r = request(constant.ENTRY_ROUTE.format(entry_id))

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exception.EntryNotFound()
    if r.html.find("h1", first=True).text == exception.SHIT_MESSAGE:
        raise exception.EntryNotFound()

    return next(utils.entry_parser(r.html))


def get_author(nickname: Nickname) -> model.Author:
    """This function get Ekşi Sözlük author.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    model.Author (class): Author data class.
    """

    r = request(constant.AUTHOR_ROUTE.format(nickname))

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exception.AuthorNotFound()

    nickname = r.html.find("h1#user-profile-title", first=True)
    biography = r.html.find("div#profile-biography", first=True)
    total_entry = r.html.find("span#entry-count-total", first=True)
    follower_count = r.html.find("span#user-follower-count", first=True)
    following_count = r.html.find("span#user-following-count", first=True)
    avatar_url = r.html.find("img.avatar", first=True)
    rank = r.html.find("p.muted", first=True)

    return model.Author(
        nickname.attrs["data-nick"],
        biography.text if biography else biography,
        int(total_entry.text),
        int(follower_count.text),
        int(following_count.text),
        avatar_url.attrs["src"],
        rank,
    )


def get_author_rank(nickname: Nickname) -> model.Rank:
    """This function get Ekşi Sözlük author rank.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    model.Rank (class): Rank data class.
    """

    author = get_author(nickname)

    return model.Rank(name=author.rank.name, karma=author.rank.karma)


def get_author_badges(nickname: Nickname) -> Iterator[model.Badge]:
    """This function get Ekşi Sözlük author badges.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    Iterator[model.Badge]: Badge data classes.
    """

    r = request(constant.AUTHOT_BADGES_TOPIC.format(nickname))

    for badge in r.html.find("li.badge-item-otheruser"):
        if badge.attrs["data-owned"] != "False":
            yield model.Badge(
                badge.find("p", first=True).text,  # name
                badge.find("a", first=True).attrs["data-title"],  # description
                badge.find("img", first=True).attrs["src"],  # icon_url
            )


def get_author_topic(nickname: Nickname, max_entry: int = None) -> model.Topic:
    """This function get Ekşi Sözlük author topic.

    Arguments:
    nickname (str): Unique author nickname.
    max_entry (int=None): Maximum number of entrys get from per page.

    Returns:
    model.Topic (class): Topic data class.
    """

    r = request(constant.AUTHOR_TOPIC_ROUTE.format(nickname))

    return get_topic(urlparse(r.url).path[1:], max_entry=max_entry)


def get_agenda(max_topic: int = None, max_entry: int = None) -> Iterator[model.Topic]:
    """This function get Ekşi Sözlük agenda (gündem) page.

    Arguments:
    max_topic (int=None): Maximum number of topics get from agenda.
    max_entry (int=None): Maximum number of entrys get from topic.

    Returns:
    Iterator[model.Topic]: Topic data classes.
    """

    r = request(constant.AGENDA_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exception.TopicNotFound()

    topic_list = r.html.find("ul.topic-list", first=True).find("a")

    for topic in topic_list[:max_topic]:
        yield get_topic(
            urlparse(topic.attrs["href"]).path.split("/")[-1],
            max_entry,
        )


def get_debe(max_entry: int = None) -> Iterator[model.Entry]:
    """This function get Ekşi Sözlük debe page.

    Arguments:
    max_entry (int=None): Maximum number of entrys get per page.

    Returns:
    Iterator[model.Topic]: Entry data classes.
    """

    r = request(constant.DEBE_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exception.EntryNotFound()

    topic_list = r.html.find("ul.topic-list", first=True).find("a")

    for topic in topic_list[:max_entry]:
        yield get_entry(
            urlparse(topic.attrs["href"]).path.split("/")[-1],
        )


def search_topic(search_keywords: SearchKeywords):
    raise NotImplementedError
