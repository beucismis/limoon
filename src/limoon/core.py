from http import HTTPStatus
from typing import Callable, Iterator, TypeVar, Optional, Union
from urllib.parse import urlparse

import requests
from requests_html import HTMLResponse, HTMLSession

from . import constant, exception, model, utils


# Typings
EntryID = TypeVar("EntryID", Callable, int)
TopicKeywords = TypeVar("TopicKeywords", Callable, str)
Nickname = TypeVar("Nickname", Callable, str)
SearchKeywords = TypeVar("SearchKeywords", Callable, str)

# Session
session = HTMLSession()


def request(endpoint: str, headers: dict = {}, params: dict = {}) -> requests.Response:
    return session.get(
        constant.BASE_URL + endpoint,
        params=params,
        headers=constant.HEADERS,
    )


def get_topic(
    topic_keywords: TopicKeywords, page: int = 1, max_entry: Optional[int] = None
) -> model.Topic:
    """This function get Ekşi Sözlük topic.

    Arguments:
    topic_keywords (str): Keywords (or path) of topic to be get.
    page (int=1): Specific topic page.
    max_entry (int|None): Max entry per topic.

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


def get_author_topic(nickname: Nickname) -> model.Topic:
    """This function get Ekşi Sözlük author topic.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    model.Topic (class): Topic data class.
    """

    r = request(constant.AUTHOR_TOPIC_ROUTE.format(nickname))

    return get_topic(urlparse(r.url).path[1:])


def get_author_last_entrys(nickname: Nickname, page: int = 1) -> Iterator[model.Entry]:
    """ """

    r = request(
        constant.AUTHOR_LAST_ENTRYS,
        params={"nick": nickname, "p": page},
    )

    topic_list = r.html.find("div#topic", first=True).find("div.topic-item")

    for topic in topic_list:
        yield get_entry(int(topic.find("li#entry-item", first=True).attrs["data-id"]))


def get_agenda(max_topic: Optional[int] = None) -> Iterator[model.Agenda]:
    """This function get Ekşi Sözlük agenda (gündem) page.

    Arguments:
    max_topic (int=None): Maximum number of topics get from agenda.

    Returns:
    Iterator[model.Agenda]: Agenda data classes.
    """

    r = request(constant.AGENDA_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exception.TopicNotFound()

    topic_list = r.html.find("ul.topic-list", first=True).find("a")

    for topic in topic_list[:max_topic]:
        yield model.Agenda(
            topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
            urlparse(topic.attrs["href"]).path.split("/")[-1],
            topic.find("small", first=True).text,
        )


def get_debe() -> Iterator[model.Debe]:
    """This function get Ekşi Sözlük debe page.

    Returns:
    Iterator[model.Debe]: Entry data classes.
    """

    r = request(constant.DEBE_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exception.EntryNotFound()

    entry_list = r.html.find("ul.topic-list", first=True).find("a")

    for entry in entry_list:
        yield model.Debe(
            entry.find("span.caption", first=True).text,
            urlparse(entry.attrs["href"]).path.split("/")[-1],
        )


def get_search_topic(keywords: SearchKeywords) -> Iterator[model.SearchResult]:
    """This function get Ekşi Sözlük search topic page.

    Arguments:
    keywords (SearchKeywords): Search keywords.

    Returns:
    Iterator[model.SearchResult]: SearchResult data classes.
    """

    r = request(
        constant.SEARCH_ROUTE,
        params={
            "SearchForm.Keywords": keywords,
            "SearchForm.NiceOnly": False,
            "SearchForm.SortOrder": "Count",
        },
    )
    total_topic = r.html.find("section#content-body", first=True)

    if total_topic.find("p")[-1].text == exception.SEARCH_SHIT_MESSAGE:
        raise exception.SearchResultNotFound()

    topic_list = r.html.find("ul.topic-list", first=True).find("a")

    for topic in topic_list:
        yield model.SearchResult(
            topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
            urlparse(topic.attrs["href"]).path.split("/")[-1],
            topic.find("small", first=True).text,
        )
