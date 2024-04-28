<img alt="limoon-logo" src="https://raw.githubusercontent.com/beucismis/limoon/main/limoon-logo.png" height="128"/>

![PyPI - Version](https://img.shields.io/pypi/v/limoon)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/limoon)
![GitHub License](https://img.shields.io/github/license/beucismis/limoon)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/test.yml?label=test)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/publish.yml?label=publish)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/doc.yml?label=doc)

Limoon (`limon-moon`, limon is lemon but Turkish), web scraper base Pythonic API for [Ekşi Sözlük](https://eksisozluk.com). This module can get topics, entries and authors. It also has `debe` and `gündem` page support. Contributions are most welcome!

## Installing

```console
pip install -U limoon
```

## Examples

```python
import limoon


topic = limoon.get_topic("richard stallman")
# Topic(43270)
list(topic.entrys)
# [Entry(1091215), Entry(1091227), Entry(2137487), ...]
dir(topic)
# [..., 'entrys', 'id', 'page_count', 'path', 'title', 'url']

entry = limoon.get_entry(2878417)
# Entry(2878417)
entry.content
# "programcılıgın 8. harikası"
dir(entry)
# [..., 'author_nickname', 'content', 'created', 'edited', 'favorite_count', 'id', 'url']

author = limoon.get_author("ssg")
# Author(ssg)
dir(author)
# [..., 'avatar_url', 'badges', 'biography', 'follower_count', 'following_count', 'nickname', 'rank', 'total_entry', 'url']
```

## Documentation

Documentation is [here](DOCUMENTATION.md). This page is auto generated. Don't edit!

## License

`limoon` is distributed under the terms of the [MIT](LICENSE.txt) license. Also the logo was made by @beucismis.
