from typing import Final

from fake_useragent import UserAgent


# Ekşi Sözlük Base URL
BASE_URL = "https://eksisozluk.com"
CDN_URL = "https://cdn.eksisozluk.com"

# Ekşi Sözlük Routes
TOPIC_ROUTE: Final = "/{}"
ENTRY_ROUTE: Final = "/entry/{}"
AUTHOR_ROUTE: Final = "/biri/{}"
AUTHOR_TOPIC_ROUTE: Final = AUTHOR_ROUTE + "/usertopic"
AUTHOT_BADGES_ROUTE: Final = "/rozetler/{}"
AUTHOR_LAST_ENTRYS_ROUTE = "/son-entryleri"
AGENDA_ROUTE: Final = "/basliklar/gundem?_=1757793708867"
DEBE_ROUTE: Final = "/debe"
SEARCH_ROUTE: Final = "/basliklar/ara"
IMAGE_ROUTE: Final = CDN_URL + "/{}/{}/{}/{}/{}.jpg"

TOTAL_ENTRY_COUNT = 300_000_000

HEADERS = {
    "User-Agent": UserAgent().random,
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
