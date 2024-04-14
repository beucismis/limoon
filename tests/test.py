import pytest

import limoon
from limoon import exception


class TestAPI:
    def test_get_topic(self):
        topic = limoon.get_topic("linux--32084")

        assert type(topic) is limoon.Topic
        assert topic.id == 32084
        assert topic.title == "linux"
        assert topic.path == "linux--32084"
        assert len(list(topic.entrys)) > 1
        assert type(list(topic.entrys)) is list
        assert topic.page_count > 1
        assert topic.url == "https://eksisozluk.com/linux--32084"

    def test_get_entry(self):
        entry = limoon.get_entry(1)

        assert type(entry) is limoon.Entry
        assert entry.id == 1
        assert entry.author_nickname == "ssg"
        assert type(entry.content) is str
        assert entry.favorite_count > 1
        assert entry.created == "15.02.1999"
        assert entry.edited == False
        assert entry.url == "https://eksisozluk.com/entry/1"

    def test_get_author(self):
        author = limoon.get_author("ssg")

        assert type(author) is limoon.Author
        assert author.nickname == "ssg"
        assert type(author.biography) is str
        assert author.total_entry > 1
        assert author.follower_count > 1
        assert author.following_count > 1
        assert "https://img.ekstat.com" in author.avatar_url
        assert type(author.rank) is limoon.Rank
        assert type(author.rank.name) is str
        assert type(author.rank.karma) is int
        assert author.url == "https://eksisozluk.com/biri/ssg"

    def test_get_author_rank(self):
        author_rank = limoon.get_author_rank("ssg")

        assert type(author_rank) is limoon.Rank
        assert type(author_rank.name) is str
        assert type(author_rank.karma) is int
        assert author_rank.karma > 1 

    def test_get_author_topic(self):
        author_topic = limoon.get_author_topic("ssg")

        assert type(author_topic) is limoon.Topic
        assert author_topic.id == 31795
        assert author_topic.title == "ssg"
        assert author_topic.path == "ssg--31795"
        assert len(list(author_topic.entrys)) > 1
        assert type(list(author_topic.entrys)) is list
        assert author_topic.page_count > 1
        assert author_topic.url == "https://eksisozluk.com/ssg--31795"


class TestException:
    def test_topic_not_found(self):
        with pytest.raises(exception.TopicNotFound):
            limoon.get_topic("böylebirbaslikyok")

    def test_entry_not_found(self):
        with pytest.raises(exception.EntryNotFound):
            limoon.get_entry(123456789)

    def test_author_not_found(self):
        with pytest.raises(exception.AuthorNotFound):
            limoon.get_author("böylebirkullanıcıyok")
