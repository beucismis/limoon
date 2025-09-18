# Table of Contents

* [limoon](#limoon)
* [limoon.models](#limoon.models)
  * [Entry](#limoon.models.Entry)
  * [Topic](#limoon.models.Topic)
  * [Rank](#limoon.models.Rank)
  * [Badge](#limoon.models.Badge)
  * [Author](#limoon.models.Author)
  * [Agenda](#limoon.models.Agenda)
  * [Debe](#limoon.models.Debe)
  * [SearchResult](#limoon.models.SearchResult)
* [limoon.utils](#limoon.utils)
* [limoon.\_\_about\_\_](#limoon.__about__)
* [limoon.exceptions](#limoon.exceptions)
  * [TopicNotFound](#limoon.exceptions.TopicNotFound)
  * [EntryNotFound](#limoon.exceptions.EntryNotFound)
  * [AuthorNotFound](#limoon.exceptions.AuthorNotFound)
  * [PageNotFound](#limoon.exceptions.PageNotFound)
  * [SearchResultNotFound](#limoon.exceptions.SearchResultNotFound)
  * [HTMLParsingError](#limoon.exceptions.HTMLParsingError)
  * [ElementNotFound](#limoon.exceptions.ElementNotFound)
* [limoon.core](#limoon.core)
  * [get\_topic](#limoon.core.get_topic)
  * [get\_entry](#limoon.core.get_entry)
  * [get\_author](#limoon.core.get_author)
  * [get\_author\_rank](#limoon.core.get_author_rank)
  * [get\_author\_badges](#limoon.core.get_author_badges)
  * [get\_author\_topic](#limoon.core.get_author_topic)
  * [get\_author\_last\_entrys](#limoon.core.get_author_last_entrys)
  * [get\_agenda](#limoon.core.get_agenda)
  * [get\_debe](#limoon.core.get_debe)
  * [get\_search\_topic](#limoon.core.get_search_topic)
  * [get\_random\_entry](#limoon.core.get_random_entry)
* [limoon.constants](#limoon.constants)

<a id="limoon"></a>

# limoon

<a id="limoon.models"></a>

# limoon.models

<a id="limoon.models.Entry"></a>

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
- `date` _str_ - Entry sting date.
- `topic_title` _str_ - Entry topic title.
- `topic_path` _str_ - Unique entry topic path.
- `created` _datetime_ - Datetime object of create entry.
- `edited` _datetime|bool_ - Datetime object of edit entry.
- `url` _str_ - Entry HTTP link.

<a id="limoon.models.Topic"></a>

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
- `entrys` _Iterator[Entry]_ - Topic total entrys per page.
- `page_count` _int|None_ - Topic total page count.
- `url` _str_ - Topic HTTP link.

<a id="limoon.models.Rank"></a>

## Rank Objects

```python
@dataclass
class Rank()
```

Rank data class.

**Arguments**:

- `name` _str_ - Custom rank name.
- `karma` _int_ - Rank karma number.

<a id="limoon.models.Badge"></a>

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

<a id="limoon.models.Author"></a>

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
- `record_date` _str_ - Author record date.
- `avatar_url` _str_ - Author avatar HTTP link.
- `rank` _class_ - Author rank.
- `badges` _class_ - Author badges.
- `url` _str_ - Author HTTP link.

<a id="limoon.models.Agenda"></a>

## Agenda Objects

```python
@dataclass
class Agenda()
```

Agenda page data class.

**Arguments**:

- `title` _str_ - Topic title.
- `path` _int_ - Unique topic path.
- `entry_count` _str_ - Topic total entry count.
- `url` _URL_ - Topic HTTP link.

<a id="limoon.models.Debe"></a>

## Debe Objects

```python
@dataclass
class Debe()
```

Depe page data class.

**Arguments**:

- `topic_title` _str_ - Topic title.
- `id` _int_ - Unique entry id.
- `url` _URL_ - Entry HTTP link.

<a id="limoon.models.SearchResult"></a>

## SearchResult Objects

```python
@dataclass
class SearchResult()
```

SearchResult data class.

**Arguments**:

- `title` _str_ - Topic title.
- `path` _str_ - Unique topic path.
- `entry_count` _str|None_ - Topic total entry count.
- `url` _URL_ - Topic HTTP link.

<a id="limoon.utils"></a>

# limoon.utils

<a id="limoon.__about__"></a>

# limoon.\_\_about\_\_

<a id="limoon.exceptions"></a>

# limoon.exceptions

<a id="limoon.exceptions.TopicNotFound"></a>

## TopicNotFound Objects

```python
class TopicNotFound(Exception)
```

The topic record is not available.

<a id="limoon.exceptions.EntryNotFound"></a>

## EntryNotFound Objects

```python
class EntryNotFound(Exception)
```

The entry record is not available.

<a id="limoon.exceptions.AuthorNotFound"></a>

## AuthorNotFound Objects

```python
class AuthorNotFound(Exception)
```

The author record is not available.

<a id="limoon.exceptions.PageNotFound"></a>

## PageNotFound Objects

```python
class PageNotFound(Exception)
```

The page record is not available.

<a id="limoon.exceptions.SearchResultNotFound"></a>

## SearchResultNotFound Objects

```python
class SearchResultNotFound(Exception)
```

Raised when no search results are found.

<a id="limoon.exceptions.HTMLParsingError"></a>

## HTMLParsingError Objects

```python
class HTMLParsingError(Exception)
```

Raised when an error occurs while parsing HTML.

<a id="limoon.exceptions.ElementNotFound"></a>

## ElementNotFound Objects

```python
class ElementNotFound(HTMLParsingError)
```

Raised when a required HTML element is not found.

<a id="limoon.core"></a>

# limoon.core

<a id="limoon.core.get_topic"></a>

#### get\_topic

```python
def get_topic(topic_keywords: TopicKeywords,
              page: int = 1,
              max_entry: Optional[int] = None) -> models.Topic
```

This function get Ekşi Sözlük topic.

**Arguments**:

- `topic_keywords` _str_ - Keywords (or path) of topic to be get.
- `page` _int=1_ - Specific topic page.
- `max_entry` _int|None_ - Max entry per topic.
  

**Returns**:

- `models.Topic` _class_ - Topic data class.

<a id="limoon.core.get_entry"></a>

#### get\_entry

```python
def get_entry(entry_id: EntryID) -> models.Entry
```

This function get Ekşi Sözlük entry.

**Arguments**:

- `entry_id` _int_ - Unique entry identity.
  

**Returns**:

- `models.Entry` _class_ - Entry data class.

<a id="limoon.core.get_author"></a>

#### get\_author

```python
def get_author(nickname: Nickname) -> models.Author
```

This function get Ekşi Sözlük author.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `models.Author` _class_ - Author data class.

<a id="limoon.core.get_author_rank"></a>

#### get\_author\_rank

```python
def get_author_rank(nickname: Nickname) -> models.Rank
```

This function get Ekşi Sözlük author rank.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `models.Rank` _class_ - Rank data class.

<a id="limoon.core.get_author_badges"></a>

#### get\_author\_badges

```python
def get_author_badges(nickname: Nickname) -> Iterator[models.Badge]
```

This function get Ekşi Sözlük author badges.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `Iterator[models.Badge]` _class_ - Badge data classes.

<a id="limoon.core.get_author_topic"></a>

#### get\_author\_topic

```python
def get_author_topic(nickname: Nickname) -> models.Topic
```

This function get Ekşi Sözlük author topic.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
  

**Returns**:

- `models.Topic` _class_ - Topic data class.

<a id="limoon.core.get_author_last_entrys"></a>

#### get\_author\_last\_entrys

```python
def get_author_last_entrys(nickname: Nickname,
                           page: int = 1) -> Iterator[models.Entry]
```

This function get Ekşi Sözlük author last entrys.

**Arguments**:

- `nickname` _str_ - Unique author nickname.
- `page` _int_ - Specific last entrys page.
  

**Returns**:

- `Iterator[models.Entry]` _class_ - Entry data class.

<a id="limoon.core.get_agenda"></a>

#### get\_agenda

```python
def get_agenda(max_topic: Optional[int] = None) -> Iterator[models.Agenda]
```

This function get Ekşi Sözlük agenda (gündem) page.

**Arguments**:

- `max_topic` _int=None_ - Maximum number of topics get from agenda.
  

**Returns**:

- `Iterator[models.Agenda]` _class_ - Agenda data classes.

<a id="limoon.core.get_debe"></a>

#### get\_debe

```python
def get_debe() -> Iterator[models.Debe]
```

This function get Ekşi Sözlük debe page.

**Returns**:

- `Iterator[models.Debe]` _class_ - Entry data classes.

<a id="limoon.core.get_search_topic"></a>

#### get\_search\_topic

```python
def get_search_topic(
        keywords: SearchKeywords) -> Iterator[models.SearchResult]
```

This function get Ekşi Sözlük search topic page.

**Arguments**:

- `keywords` _SearchKeywords_ - Search keywords.
  

**Returns**:

- `Iterator[models.SearchResult]` _class_ - SearchResult data classes.

<a id="limoon.core.get_random_entry"></a>

#### get\_random\_entry

```python
def get_random_entry() -> models.Entry
```

This function get random entry.

**Returns**:

- `models.Entry` _class_ - Entry data classes.

<a id="limoon.constants"></a>

# limoon.constants

