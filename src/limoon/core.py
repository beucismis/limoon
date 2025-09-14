from http import HTTPStatus
from typing import Callable, Iterator, Optional, TypeVar, Union
from urllib.parse import urlparse

import requests
from requests_html import HTMLResponse, HTMLSession

from . import constants, exceptions, models, utils


# Typings
EntryID = TypeVar("EntryID", Callable, int)
TopicKeywords = TypeVar("TopicKeywords", Callable, str)
Nickname = TypeVar("Nickname", Callable, str)
SearchKeywords = TypeVar("SearchKeywords", Callable, str)

# Session
session = HTMLSession()


def request(endpoint: str, headers: dict = {}, params: dict = {}) -> requests.Response:
    return session.get(
        constants.BASE_URL + endpoint,
        params=params,
        headers=constants.HEADERS,
    )


def get_topic(
    topic_keywords: TopicKeywords, page: int = 1, max_entry: Optional[int] = None
) -> models.Topic:
    """This function get Ekşi Sözlük topic.

    Arguments:
    topic_keywords (str): Keywords (or path) of topic to be get.
    page (int=1): Specific topic page.
    max_entry (int|None): Max entry per topic.

    Returns:
    models.Topic (class): Topic data class.
    """

    if not isinstance(page, int):
        raise TypeError

    r = request(constants.TOPIC_ROUTE.format(topic_keywords), params={"p": page})

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exceptions.TopicNotFound()

    h1 = r.html.find("h1#title", first=True)
    path = h1.find("a", first=True).attrs["href"]
    page_count = r.html.find("div.pager", first=True)

    return models.Topic(
        int(h1.attrs["data-id"]),
        h1.attrs["data-title"],
        path[1:],
        utils.entry_parser(r.html, max_entry),
        int(page_count.attrs["data-pagecount"]) if page_count else page_count,
    )


def get_entry(entry_id: EntryID) -> models.Entry:
    """This function get Ekşi Sözlük entry.

    Arguments:
    entry_id (int): Unique entry identity.

    Returns:
    models.Entry (class): Entry data class.
    """

    if not isinstance(entry_id, int):
        raise TypeError

    r = request(constants.ENTRY_ROUTE.format(entry_id))

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exceptions.EntryNotFound()
    if r.html.find("h1", first=True).text == exceptions.SHIT_MESSAGE:
        raise exceptions.EntryNotFound()

    return next(utils.entry_parser(r.html))


def get_author(nickname: Nickname) -> models.Author:
    """This function get Ekşi Sözlük author.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    models.Author (class): Author data class.
    """

    r = request(constants.AUTHOR_ROUTE.format(nickname))

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exceptions.AuthorNotFound()

    nickname = r.html.find("h1#user-profile-title", first=True)
    biography = r.html.find("div#profile-biography", first=True)
    total_entry = r.html.find("span#entry-count-total", first=True)
    follower_count = r.html.find("span#user-follower-count", first=True)
    following_count = r.html.find("span#user-following-count", first=True)
    record_date = r.html.find("div.recorddate", first=True)
    avatar_url = r.html.find("img.avatar", first=True)
    rank = r.html.find("p.muted", first=True)

    return models.Author(
        nickname.attrs["data-nick"],
        biography.text if biography else biography,
        int(total_entry.text),
        int(follower_count.text),
        int(following_count.text),
        record_date.text.title(),
        avatar_url.attrs["src"],
        rank,
    )


def get_author_rank(nickname: Nickname) -> models.Rank:
    """This function get Ekşi Sözlük author rank.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    models.Rank (class): Rank data class.
    """

    author = get_author(nickname)

    return models.Rank(name=author.rank.name, karma=author.rank.karma)


def get_author_badges(nickname: Nickname) -> Iterator[models.Badge]:
    """This function get Ekşi Sözlük author badges.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    Iterator[models.Badge]: Badge data classes.
    """

    r = request(constants.AUTHOT_BADGES_ROUTE.format(nickname))

    for badge in r.html.find("li.badge-item-otheruser"):
        if badge.attrs["data-owned"] != "False":
            yield models.Badge(
                badge.find("p", first=True).text,  # name
                badge.find("a", first=True).attrs["data-title"],
                badge.find("img", first=True).attrs["src"],
            )


def get_author_topic(nickname: Nickname) -> models.Topic:
    """This function get Ekşi Sözlük author topic.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    models.Topic (class): Topic data class.
    """

    r = request(constants.AUTHOR_TOPIC_ROUTE.format(nickname))

    return get_topic(urlparse(r.url).path[1:])


def get_author_last_entrys(nickname: Nickname, page: int = 1) -> Iterator[models.Entry]:
    """ """

    r = request(
        constants.AUTHOR_LAST_ENTRYS_ROUTE,
        params={"nick": nickname, "p": page},
    )

    topic_list = r.html.find("div#topic", first=True).find("div.topic-item")

    for topic in topic_list:
        yield get_entry(int(topic.find("li#entry-item", first=True).attrs["data-id"]))


def get_agenda(max_topic: Optional[int] = None) -> Iterator[models.Agenda]:
    """This function get Ekşi Sözlük agenda (gündem) page.

    Arguments:
    max_topic (int=None): Maximum number of topics get from agenda.

    Returns:
    Iterator[models.Agenda]: Agenda data classes.
    """

    r = request(constants.AGENDA_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exceptions.TopicNotFound()

    topic_list = r.html.find("ul.topic-list", first=True).find("a")

    for topic in topic_list[:max_topic]:
        yield models.Agenda(
            topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
            urlparse(topic.attrs["href"]).path.split("/")[-1],
            topic.find("small", first=True).text,
        )


def get_debe() -> Iterator[models.Debe]:
    """This function get Ekşi Sözlük debe page.

    Returns:
    Iterator[models.Debe]: Entry data classes.
    """

    r = request(constants.DEBE_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exceptions.EntryNotFound()

    entry_list = r.html.find("ul.topic-list", first=True).find("a")

    for entry in entry_list:
        yield models.Debe(
            entry.find("span.caption", first=True).text,
            urlparse(entry.attrs["href"]).path.split("/")[-1],
        )


def get_search_topic(keywords: SearchKeywords) -> Iterator[models.SearchResult]:
    """This function get Ekşi Sözlük search topic page.

    Arguments:
    keywords (SearchKeywords): Search keywords.

    Returns:
    Iterator[models.SearchResult]: SearchResult data classes.
    """

    r = request(
        constants.SEARCH_ROUTE,
        params={
            "SearchForm.Keywords": keywords,
            "SearchForm.NiceOnly": "false",
            "SearchForm.SortOrder": "Count",
        },
    )

    topic_ul = r.html.find("ul.topic-list", first=True)

    if not topic_ul:
        raise exceptions.SearchResultNotFound()

    topic_list = topic_ul.find("a")

    for topic in topic_list:
        yield models.SearchResult(
            topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
            urlparse(topic.attrs["href"]).path.split("/")[-1],
            topic.find("small", first=True).text,
        )
