from typing import Iterator

from requests_html import HTML, Element

from limoon import model


def extract_entry_data(element: Element) -> list:
    author = element.find("a.entry-author", first=True)
    content = element.find("div.content", first=True)
    favorite_count = element.attrs["data-favorite-count"]
    created = element.find("a.entry-date", first=True)

    return [
        int(element.attrs["data-id"]),
        author.text,
        content.text,
        int(favorite_count),
        created.text,
    ]


def entry_parser(html: HTML, max_entry: int = None) -> Iterator[model.Entry]:
    entry_items = html.find("ul#entry-item-list", first=True).find("li#entry-item")

    for item in entry_items[:max_entry]:
        entry_data = extract_entry_data(item)
        yield model.Entry(*entry_data)
