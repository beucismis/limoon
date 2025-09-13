from typing import Final

from fake_useragent import UserAgent


# Ekşi Sözlük Base URL
BASE_URL = "https://eksisozluk.com"

# Ekşi Sözlük Routes
TOPIC_ROUTE: Final = "/{}"
ENTRY_ROUTE: Final = "/entry/{}"
AUTHOR_ROUTE: Final = "/biri/{}"
AUTHOR_TOPIC_ROUTE: Final = AUTHOR_ROUTE + "/usertopic"
AUTHOT_BADGES_TOPIC: Final = "/rozetler/{}"
AUTHOR_LAST_ENTRYS = "/son-entryleri"
AGENDA_ROUTE: Final = "/basliklar/gundem"
DEBE_ROUTE: Final = "/debe"
SEARCH_ROUTE: Final = "/basliklar/ara"

HEADERS = {
    "User-Agent": UserAgent().random,
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
