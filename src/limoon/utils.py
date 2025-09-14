from urllib.parse import urlparse
from typing import Optional, Iterator

from requests_html import HTML

from . import model


def entry_parser(html: HTML, max_entry: Optional[int] = None) -> Iterator[model.Entry]:
    entry_items = html.find("ul#entry-item-list", first=True).find("li#entry-item")

    for item in entry_items[:max_entry]:
        author = item.find("a.entry-author", first=True)
        content = item.find("div.content", first=True)
        favorite_count = item.attrs["data-favorite-count"]
        created = item.find("a.entry-date", first=True)
        topic_title = html.find("h1#title", first=True)

        yield model.Entry(
            int(item.attrs["data-id"]),
            author.text,
            content.text,
            int(favorite_count),
            created.text,
            topic_title.attrs["data-title"],
            urlparse(topic_title.find("a", first=True).attrs["href"]).path.split("/")[-1]
        )
