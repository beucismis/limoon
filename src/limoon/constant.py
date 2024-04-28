from typing import Final

# Ekşi Sözlük Base URL
BASE_URL = "https://eksisozluk.com"

# Ekşi Sözlük Routes
TOPIC_ROUTE: Final = "/{}"
ENTRY_ROUTE: Final = "/entry/{}"
AUTHOR_ROUTE: Final = "/biri/{}"
AUTHOR_TOPIC_ROUTE: Final = AUTHOR_ROUTE + "/usertopic"
AUTHOT_BADGES_TOPIC: Final = "/rozetler/{}"
AGENDA_ROUTE: Final = "/basliklar/gundem"
DEBE_ROUTE: Final = "/debe"
SEARCH_ROUTE: Final = "/basliklar/ara"
