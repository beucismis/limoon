from datetime import datetime
from types import NoneType

import pytest

from src import limoon


class TestAPI:
    def test_base_url(self):
        limoon.BASE_URL = "https://eksisozluk1923.com"
        assert limoon.BASE_URL == "https://eksisozluk1923.com"

    def test_get_topic(self):
        topic = limoon.get_topic("linux--32084")

        assert type(topic) is limoon.Topic
        assert topic.id == 32084
        assert topic.title == "linux"
        assert topic.path == "linux--32084"
        assert topic.page_count > 1
        assert topic.url == "https://eksisozluk.com/linux--32084"

    def test_get_topic_page(self):
        topic = limoon.get_topic("linux--32084", page=42)
        entrys = list(topic.entrys)

        assert len(entrys) == 10
        assert topic.page_count > 1
        assert entrys[1].author_nickname == "hooker with a penis"
        assert "linux çekirdektir." in entrys[1].text

    def test_get_entry(self):
        entry = limoon.get_entry(1)

        assert type(entry) is limoon.Entry
        assert entry.id == 1
        assert entry.author_nickname == "ssg"
        assert type(entry.text) is str
        assert type(entry.html) is str
        assert entry.favorite_count > 1
        assert entry.topic_title == "pena"
        assert entry.topic_path == "pena--31782"
        assert entry.is_pinned == False
        assert entry.is_pinned_on_profile == False
        assert entry.created == datetime.strptime("15.02.1999", "%d.%m.%Y")
        assert entry.edited == False
        assert entry.url == "https://eksisozluk.com/entry/1"

    def test_get_entry_image(self):
        entry = limoon.get_entry(145946967)

        assert entry.images[0] == "https://soz.lk/i/hw9d8bdw"
        assert entry.images_source[0] == "https://cdn.eksisozluk.com/2022/12/5/h/hw9d8bdw.jpg"

    def test_get_author(self):
        author = limoon.get_author("ekşisözlük")

        assert type(author) is limoon.Author
        assert author.nickname == "ekşisözlük"
        assert type(author.biography_text) is NoneType
        assert type(author.biography_html) is NoneType
        assert author.total_entry > 1
        assert author.follower_count > 1
        assert author.following_count == 0
        assert author.record_date == "Şubat 1999"
        assert "https://img.ekstat.com" in author.avatar_url
        assert author.url == "https://eksisozluk.com/biri/ekşisözlük"

    def test_get_author_rank(self):
        author_rank = limoon.get_author_rank("ssg")

        assert type(author_rank) is limoon.Rank
        assert type(author_rank.name) is str
        assert type(author_rank.karma) is int
        assert author_rank.karma > 1

    def test_get_author_badges(self):
        author_badges = list(limoon.get_author_badges("ssg"))

        assert type(author_badges) is list
        assert type(author_badges[0]) is limoon.Badge
        assert type(author_badges[0].name) is str
        assert type(author_badges[0].description) is str
        assert type(author_badges[0].icon_url) is str

    def test_get_author_topic(self):
        author_topic = limoon.get_author_topic("ssg")

        assert type(author_topic) is limoon.Topic
        assert author_topic.id == 31795
        assert author_topic.title == "ssg"
        assert author_topic.path == "ssg--31795"
        assert author_topic.page_count > 1
        assert author_topic.url == "https://eksisozluk.com/ssg--31795"

    def test_get_agenda(self):
        agenda = list(limoon.get_agenda())[0]
        assert type(agenda) is limoon.Agenda

    def test_get_debe(self):
        debe = list(limoon.get_debe())[0]
        assert type(debe) is limoon.Debe

    def test_get_search_topic(self):
        search_result = list(limoon.get_search_topic("linux"))[0]

        assert type(search_result) is limoon.SearchResult
        assert search_result.title == "linux"
        assert search_result.path == "linux--32084"
        assert type(search_result.entry_count) is str
        assert search_result.url == "https://eksisozluk.com/linux--32084"


class TestException:
    def test_topic_not_found(self):
        with pytest.raises(limoon.TopicNotFound):
            limoon.get_topic("böylebirbaslikyok")

    def test_topic_page_not_found(self):
        with pytest.raises(limoon.TopicNotFound):
            limoon.get_topic("linux--32084", page=123456789)

    def test_entry_not_found(self):
        with pytest.raises(limoon.EntryNotFound):
            limoon.get_entry(123456789)

    def test_author_not_found(self):
        with pytest.raises(limoon.AuthorNotFound):
            limoon.get_author("böylebirkullanıcıyok")
