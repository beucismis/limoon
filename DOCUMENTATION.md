# Table of Contents

* [limoon](#limoon)
* [limoon.core](#limoon.core)
  * [get\_topic](#limoon.core.get_topic)
  * [get\_entry](#limoon.core.get_entry)
  * [get\_author](#limoon.core.get_author)
  * [get\_author\_rank](#limoon.core.get_author_rank)
  * [get\_author\_badges](#limoon.core.get_author_badges)
  * [get\_author\_topic](#limoon.core.get_author_topic)
  * [get\_agenda](#limoon.core.get_agenda)
  * [get\_debe](#limoon.core.get_debe)
* [limoon.utils](#limoon.utils)
* [limoon.constant](#limoon.constant)
* [limoon.model](#limoon.model)
  * [Entry](#limoon.model.Entry)
  * [Topic](#limoon.model.Topic)
  * [Rank](#limoon.model.Rank)
  * [Badge](#limoon.model.Badge)
  * [Author](#limoon.model.Author)
* [limoon.exception](#limoon.exception)
  * [TopicNotFound](#limoon.exception.TopicNotFound)
  * [EntryNotFound](#limoon.exception.EntryNotFound)
  * [AuthorNotFound](#limoon.exception.AuthorNotFound)
  * [PageNotFound](#limoon.exception.PageNotFound)

<a id="limoon"></a>

# limoon

<a id="limoon.core"></a>

# limoon.core

<a id="limoon.core.get_topic"></a>

#### get\_topic

```python
def get_topic(topic_keywords: TopicKeywords,
              max_entry: int = None,
              page: int = 1) -> model.Topic
```

This function get Ekşi Sözlük topic.

**Arguments**:

- `topic_keywords` _str_ - Keywords (or path) of topic to be get.
- `max_entry` _int=None_ - Maximum number of entrys get from per page.
- `page` _int=1_ - Specific topic page.
  

**Returns**:

- `model.Topic` _class_ - Topic data class.

<a id="limoon.core.get_entry"></a>

#### get\_entry

```python
def get_entry(entry_id: EntryID) -> model.Entry
```

This function get Ekşi Sözlük entry.

**Arguments**:

- `entry_id` _int_ - Unique entry identity.
  

**Returns**:

- `model.Entry` _class_ - Entry data class.

<a id="limoon.core.get_author"></a>

#### get\_author

```python
def get_author(nickname: Nickname) -> model.Author
```

This function get Ekşi Sözlük author.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `model.Author` _class_ - Author data class.

<a id="limoon.core.get_author_rank"></a>

#### get\_author\_rank

```python
def get_author_rank(nickname: Nickname) -> model.Rank
```

This function get Ekşi Sözlük author rank.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `model.Rank` _class_ - Rank data class.

<a id="limoon.core.get_author_badges"></a>

#### get\_author\_badges

```python
def get_author_badges(nickname: Nickname) -> Iterator[model.Badge]
```

This function get Ekşi Sözlük author badges.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `Iterator[model.Badge]` - Badge data classes.

<a id="limoon.core.get_author_topic"></a>

#### get\_author\_topic

```python
def get_author_topic(nickname: Nickname, max_entry: int = None) -> model.Topic
```

This function get Ekşi Sözlük author topic.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
- `max_entry` _int=None_ - Maximum number of entrys get from per page.
  

**Returns**:

- `model.Topic` _class_ - Topic data class.

<a id="limoon.core.get_agenda"></a>

#### get\_agenda

```python
def get_agenda(max_topic: int = None,
               max_entry: int = None) -> Iterator[model.Topic]
```

This function get Ekşi Sözlük agenda (gündem) page.

**Arguments**:

- `max_topic` _int=None_ - Maximum number of topics get from agenda.
- `max_entry` _int=None_ - Maximum number of entrys get from topic.
  

**Returns**:

- `Iterator[model.Topic]` - Topic data classes.

<a id="limoon.core.get_debe"></a>

#### get\_debe

```python
def get_debe(max_entry: int = None) -> Iterator[model.Entry]
```

This function get Ekşi Sözlük debe page.

**Arguments**:

- `max_entry` _int=None_ - Maximum number of entrys get per page.
  

**Returns**:

- `Iterator[model.Topic]` - Entry data classes.

<a id="limoon.utils"></a>

# limoon.utils

<a id="limoon.constant"></a>

# limoon.constant

<a id="limoon.model"></a>

# limoon.model

<a id="limoon.model.Entry"></a>

## Entry Objects

```python
@dataclass
class Entry()
```

Entry data class.

**Arguments**:

- `id` _int_ - Unique entry identity.
- `author_nickname` _str_ - Author who created entry.
- `content` _str_ - Entry content (with HTML tags).
- `favorite_count` _int_ - Entry favorite count.
- `created` _str_ - Datetime of create entry.
- `edited` _str|bool_ - Datetime of edit entry.
- `url` _str_ - Entry HTTP link.

<a id="limoon.model.Topic"></a>

## Topic Objects

```python
@dataclass
class Topic()
```

Topic data class.

**Arguments**:

- `id` _int_ - Unique topic identity.
- `title` _str_ - Topic title.
- `path` _str_ - Unique topic path.
- `entrys` _class_ - Entrys written for topic.
- `page_count` _int|None_ - Topic total page count.
- `url` _str_ - Topic HTTP link.

<a id="limoon.model.Rank"></a>

## Rank Objects

```python
@dataclass
class Rank()
```

Rank data class.

**Arguments**:

- `name` _str_ - Custom rank name.
- `karma` _int_ - Rank karma number.

<a id="limoon.model.Badge"></a>

## Badge Objects

```python
@dataclass
class Badge()
```

Badge data class.

**Arguments**:

  name (str):
  description (str):
  icon_url (str):

<a id="limoon.model.Author"></a>

## Author Objects

```python
@dataclass
class Author()
```

Author data class.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
- `biography` _str|None_ - Author biography (with HTML tags).
- `total_entry` _int_ - Author total entry count.
- `follower_count` _int_ - Author total follower count.
- `following_count` _int_ - Author total following count.
- `avatar_url` _str_ - Author avatar HTTP link.
- `rank` _class_ - Author rank.
- `badges` _class_ - Author badges.
- `url` _str_ - Author HTTP link.

<a id="limoon.exception"></a>

# limoon.exception

<a id="limoon.exception.TopicNotFound"></a>

## TopicNotFound Objects

```python
class TopicNotFound(Exception)
```

The topic record is not available.

<a id="limoon.exception.EntryNotFound"></a>

## EntryNotFound Objects

```python
class EntryNotFound(Exception)
```

The entry record is not available.

<a id="limoon.exception.AuthorNotFound"></a>

## AuthorNotFound Objects

```python
class AuthorNotFound(Exception)
```

The author record is not available.

<a id="limoon.exception.PageNotFound"></a>

## PageNotFound Objects

```python
class PageNotFound(Exception)
```

The page record is not available.

