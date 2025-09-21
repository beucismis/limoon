import re
from typing import Iterator, Optional
from urllib.parse import urlparse

from requests_html import HTML

from . import models


def find_image_url(html: str) -> Optional[list]:
    pattern = r'href="(https://soz\.lk/i/[a-zA-Z0-9]+)"'
    matches = re.findall(pattern, html)

    if matches:
        return matches
    return None


def entry_parser(html: HTML, max_entry: Optional[int] = None) -> Iterator[models.Entry]:
    entry_items = html.find("ul#entry-item-list", first=True).find("li#entry-item")

    for item in entry_items[:max_entry]:
        author = item.find("a.entry-author", first=True)
        content = item.find("div.content", first=True)
        favorite_count = item.attrs["data-favorite-count"]
        created = item.find("a.entry-date", first=True)
        topic_title = html.find("h1#title", first=True)
        topic_path = topic_title.find("a", first=True).attrs["href"]
        is_pinned = item.attrs["data-ispinned"]
        is_pinned_on_profile = item.attrs["data-ispinnedonprofile"]

        yield models.Entry(
            int(item.attrs["data-id"]),
            author.text,
            content.text,
            content.html,
            int(favorite_count),
            created.text,
            topic_title.attrs["data-title"],
            urlparse(topic_path).path.split("/")[-1],
            True if is_pinned == "true" else False,
            True if is_pinned_on_profile == "true" else False,
            find_image_url(content.html),
        )
