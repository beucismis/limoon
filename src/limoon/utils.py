from typing import Iterator

from requests_html import HTML

from limoon import model


def entry_parser(html: HTML, max_entry: int = None) -> Iterator[model.Entry]:
    entry_items = html.find("ul#entry-item-list", first=True).find("li#entry-item")

    for item in entry_items[:max_entry]:
        author = item.find("a.entry-author", first=True)
        content = item.find("div.content", first=True)
        favorite_count = item.attrs["data-favorite-count"]
        created = item.find("a.entry-date", first=True)

        yield model.Entry(
            int(item.attrs["data-id"]),
            author.text,
            content.text,
            int(favorite_count),
            created.text,
        )
