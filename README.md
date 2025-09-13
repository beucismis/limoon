<p align="center" width="100%">
<img height="128" src="https://github.com/user-attachments/assets/4c1f51e0-a7e8-47f3-b311-d828a6765b09" alt="limoon-logo" />
</p>

Limoon (`limon-moon`, limon is lemon but Turkish), web scraper base Pythonic API for [Ekşi Sözlük](https://eksisozluk.com). This module can get topics, entries and authors. It also has `debe` and `gündem` page support. Contributions are most welcome!

![PyPI - Version](https://img.shields.io/pypi/v/limoon)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/limoon)
![GitHub License](https://img.shields.io/github/license/beucismis/limoon)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/test.yml?label=test)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/publish.yml?label=publish)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beucismis/limoon/doc.yml?label=doc)

## Installing

```
pip install -U limoon
```

## Examples

```python
import limoon


limoon.BASE_URL = "https://eksisozluk1923.com"
print(limoon.BASE_URL)
# 'https://eksisozluk1923.com'

topic = limoon.get_topic("richard stallman")
# Topic(43270)
dir(topic)
# [..., 'id', 'page_count', 'path', 'title', 'url']

entry = limoon.get_entry(2878417)
# Entry(2878417)
entry.content
# 'programcılıgın 8. harikası'
dir(entry)
# [..., 'author_nickname', 'content', 'created', 'date', 'edited', 'favorite_count', 'id', 'url']

author = limoon.get_author("ssg")
# Author(ssg)
dir(author)
# [..., 'avatar_url', 'badges', 'biography', 'follower_count', 'following_count', 'nickname', 'rank', 'total_entry', 'url']

search_result = limoon.get_search_topic("linux")
# Iterator[SearchResult]
list(search_result)
# [SearchResult(linux), SearchResult(linux mint), SearchResult(arch linux), SearchResult(linux ile windows karşılaştırması), SearchResult(linux kullanabilen kız), ...]
```

## Documentation

Documentation is [here](DOCUMENTATION.md). This page is auto generated. Don't edit!

## License

`limoon` is distributed under the terms of the [MIT](LICENSE.txt) license. Also the logo was made by @beucismis.
