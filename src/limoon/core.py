import random
from http import HTTPStatus
from typing import Callable, Iterator, Optional, TypeVar, Union
from urllib.parse import urlparse

import requests
from curl_adapter import CurlCffiAdapter
from requests_html import HTMLResponse, HTMLSession

from . import constants, exceptions, models, utils


# Typings
EntryID = TypeVar("EntryID", Callable, int)
TopicKeywords = TypeVar("TopicKeywords", Callable, str)
Nickname = TypeVar("Nickname", Callable, str)
SearchKeywords = TypeVar("SearchKeywords", Callable, str)

# Session
session = HTMLSession()
session.mount("http://", CurlCffiAdapter())
session.mount("https://", CurlCffiAdapter())


def request(endpoint: str, headers: dict = {}, params: dict = {}) -> requests.Response:
    return session.get(
        constants.BASE_URL + endpoint,
        params=params,
        headers=constants.HEADERS,
    )


def get_topic(
    topic_keywords: TopicKeywords,
    page: int = 1,
    action: Optional[str] = None,
    day: Optional[str] = None,
    max_entry: Optional[int] = None,
) -> models.Topic:
    """This function get Ekşi Sözlük topic.

    Arguments:
    topic_keywords (str): Keywords (or path) of topic to be get.
    page (int=1): Specific topic page.
    action (str|None): Nice or popular.
    day (str|None): Specific entry day.
    max_entry (int|None): Max entry per topic.

    Returns:
    models.Topic (class): Topic data class.
    """

    if not isinstance(page, int):
        raise TypeError

    params = {"p": page}

    if action in ("nice", "popular"):
        params["a"] = action

    if day:
        params["day"] = day

    r = request(
        constants.TOPIC_ROUTE.format(topic_keywords),
        params=params,
    )

    if r.status_code == HTTPStatus.NOT_FOUND:
        raise exceptions.TopicNotFound()

    try:
        h1 = r.html.find("h1#title", first=True)
        path = h1.find("a", first=True).attrs["href"]
        page_count = r.html.find("div.pager", first=True)

        return models.Topic(
            int(h1.attrs["data-id"]),
            h1.attrs["data-title"],
            path[1:],
            utils.entry_parser(r.html, max_entry),
            0 if page_count is None else int(page_count.attrs["data-pagecount"]),
        )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse topic page: {e}", html=r.html.html)


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

    try:
        return next(utils.entry_parser(r.html))
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse entry page: {e}", html=r.html.html)


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

    try:
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
            biography.html if biography else biography,
            int(total_entry.text),
            int(follower_count.text),
            int(following_count.text),
            record_date.text.title(),
            avatar_url.attrs["src"],
            rank,
        )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse author page: {e}", html=r.html.html)


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
    Iterator[models.Badge] (class): Badge data classes.
    """

    r = request(constants.AUTHOT_BADGES_ROUTE.format(nickname))

    try:
        for badge in r.html.find("li.badge-item-otheruser"):
            if badge.attrs["data-owned"] != "False":
                yield models.Badge(
                    badge.find("p", first=True).text,
                    badge.find("a", first=True).attrs["data-title"],
                    badge.find("img", first=True).attrs["src"],
                )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse author badges page: {e}", html=r.html.html)


def get_author_topic(nickname: Nickname) -> models.Topic:
    """This function get Ekşi Sözlük author topic.

    Arguments:
    nickname (str): Unique author nickname.

    Returns:
    models.Topic (class): Topic data class.
    """

    r = request(constants.AUTHOR_TOPIC_ROUTE.format(nickname))

    return get_topic(urlparse(r.url).path[1:])


def get_author_last_entrys(nickname: Nickname, page: int = 1) -> Optional[Iterator[models.Entry]]:
    """This function get Ekşi Sözlük author last entrys.

    Arguments:
    nickname (str): Unique author nickname.
    page (int=1): Specific last entrys page.

    Returns:
    Iterator[models.Entry] (class|None): Entry data class.
    """

    r = request(
        constants.AUTHOR_LAST_ENTRYS_ROUTE,
        params={"nick": nickname, "p": page},
    )

    try:
        topic_list = r.html.find("div#topic", first=True)

        if topic_list is None:
            return None

        for topic in topic_list.find("div.topic-item"):
            yield get_entry(int(topic.find("li#entry-item", first=True).attrs["data-id"]))
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse author last entrys page: {e}", html=r.html.html)


def get_agenda(max_topic: Optional[int] = None, page: int = 1) -> Iterator[models.Agenda]:
    """This function get Ekşi Sözlük agenda (gündem) page.

    Arguments:
    max_topic (int|None): Maximum number of topics get from agenda.
    page (int=1): Specific topic agenda page.

    Returns:
    Iterator[models.Agenda] (class): Agenda data classes.
    """

    r = request(constants.AGENDA_ROUTE, params={"p": page})

    if r.status_code != HTTPStatus.OK:
        raise exceptions.TopicNotFound()

    try:
        topic_list = r.html.find("ul.topic-list", first=True).find("a")

        for topic in topic_list[:max_topic]:
            yield models.Agenda(
                topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
                urlparse(topic.attrs["href"]).path.split("/")[-1],
                topic.find("small", first=True).text,
            )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse agenda page: {e}", html=r.html.html)


def get_debe() -> Iterator[models.Debe]:
    """This function get Ekşi Sözlük debe page.

    Returns:
    Iterator[models.Debe] (class): Entry data classes.
    """

    r = request(constants.DEBE_ROUTE)

    if r.status_code != HTTPStatus.OK:
        raise exceptions.EntryNotFound()

    try:
        entry_list = r.html.find("ul.topic-list", first=True).find("a")

        for entry in entry_list:
            yield models.Debe(
                entry.find("span.caption", first=True).text,
                urlparse(entry.attrs["href"]).path.split("/")[-1],
            )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse debe page: {e}", html=r.html.html)


def get_search_topic(keywords: SearchKeywords) -> Iterator[models.SearchResult]:
    """This function get Ekşi Sözlük search topic page.

    Arguments:
    keywords (SearchKeywords): Search keywords.

    Returns:
    Iterator[models.SearchResult] (class): SearchResult data classes.
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

    try:
        topic_list = topic_ul.find("a")

        for topic in topic_list:
            yield models.SearchResult(
                topic.element.xpath("text()")[0].strip(),
                urlparse(topic.attrs["href"]).path.split("/")[-1],
                topic.find("small", first=True).text if topic.find("small", first=True) else None,
            )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse search topic page: {e}", html=r.html.html)


def get_random_entry() -> models.Entry:
    """This function get random entry.

    Returns:
    models.Entry (class): Entry data classes.
    """

    return get_entry(random.randint(1, constants.TOTAL_ENTRY_COUNT))


def get_channel(name: str, max_topic: Optional[int] = None) -> Iterator[models.ChannelTopic]:
    """This function get channel topics.

    Arguments:
    name (str): Channel name.
    max_topic (int|None): Maximum number of topics get from agenda.

    Returns:
    Iterator[models.ChannelTopic (class): ChannelTopic data classes.
    """

    if not name in [channel.name for channel in constants.CHANNELS]:
        raise exceptions.ChannelNotFound()

    r = request(constants.CHANNEL_ROUTE.format(name))

    try:
        topic_list = r.html.find("ul.topic-list", first=True).find("a")

        for topic in topic_list[:max_topic]:
            yield models.ChannelTopic(
                name,
                topic.text.rsplit(None, 1)[0] if " " in topic.text else "",
                urlparse(topic.attrs["href"]).path.split("/")[-1],
                urlparse(topic.attrs["href"]).query.split("=")[-1],
                topic.find("small", first=True).text if topic.find("small", first=True) else None,
            )
    except AttributeError as e:
        raise exceptions.ElementNotFound(message=f"Failed to parse channel page: {e}", html=r.html.html)
