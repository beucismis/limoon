from typing import Final

from fake_useragent import UserAgent

from .models import Channel


# Ekşi Sözlük Base URL
BASE_URL = "https://eksisozluk.com"
CDN_URL = "https://cdn.eksisozluk.com"

HEADERS = {
    "User-Agent": UserAgent().random,
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

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
CHANNEL_ROUTE: Final = "/basliklar/kanal/{}"

TOTAL_ENTRY_COUNT = 300_000_000

CHANNELS = [
    Channel("haber", "yurtta ve dünyada olan biten", "haber"),
    Channel(
        "sinema",
        "filmler, yönetmenler, teknikler, yarıda salonu terk etmeler",
        "sinema",
    ),
    Channel("bilim", "atom mühendisliğine giden yolda her konu", "bilim"),
    Channel("eğitim", "akademi, müfredat, hocalar ve dersler", "egitim"),
    Channel(
        "müzik",
        "gruplar, parçalar, müzik teorileri, enstrümanlar, pena",
        "muzik",
    ),
    Channel(
        "spoiler",
        "bozan, heves kaçıran her türlü bilgi. bu arada bruce willis ölüymüş.",
        "spoiler",
    ),
    Channel(
        "edebiyat",
        "kitaplar, yazarlar, ekoller, yayıncılar, ödüller ve niceleri",
        "edebiyat",
    ),
    Channel(
        "ekonomi",
        "finans, yatırım araçları, krizler, bankalar, parasal göstergeler",
        "ekonomi",
    ),
    Channel("tarih", "geçmişten günümüze hayatlar, insanlar", "tarih"),
    Channel(
        "yeme-içme",
        "restoranlar, mekanlar, yemekler ve yanında içilecekler",
        "yeme icme",
    ),
    Channel("ilişkiler", "sevgili, eski sevgili ve hoşlanılan kız", "iliskiler"),
    Channel(
        "teknoloji",
        "cihazlar, yazılımlar, standartlar, mavi ekran",
        "teknoloji",
    ),
    Channel(
        "siyaset",
        "partiler, politikacılar, terör, savaş kan ve korku",
        "siyaset",
    ),
    Channel("sanat", "teoriler, sanatçılar, sanat tarihi, ucubeler", "sanat"),
    Channel("moda", "giyim, kuşam, takıp takıştırma", "moda"),
    Channel(
        "otomotiv",
        "araba markaları, modelleri, konseptler, jargon",
        "otomotiv",
    ),
    Channel(
        "magazin",
        "normalde kimseyi ilgilendirmeyen ama içinde sırf ünlü var diye anlamlı olan saçma şeyler",
        "magazin",
    ),
    Channel("spor", "futbol, basketbol, tenis ve curling gibi ata sporları", "spor"),
    Channel("ekşi-sözlük", "bizzat ekşi sözlük hakkında", "eksi sozluk"),
    Channel(
        "motosiklet",
        "motorculuk dünyası, markalar, modeller, kulüpler",
        "motosiklet",
    ),
    Channel(
        "sağlık",
        "rahatsızlıklar, hastalıklar, ilaçlar, tedaviler, anatomi, hurafeler",
        "saglik",
    ),
    Channel(
        "oyun",
        "video oyunları, konsollar, oyuncular, efsaneler, atari",
        "oyun",
    ),
    Channel("anket", "subjektif cevap yığınları", "anket"),
    Channel(
        "programlama",
        "yazılım geliştirme jargonu, araçları, teknikler, atasözleri",
        "programlama",
    ),
    Channel("tv", "tv kanalları, diziler, yarışmalar", "tv"),
    Channel("seyahat", "gezilecek, görülecek yerlerle ilgili her şey", "seyahat"),
    Channel(
        "havacılık",
        "hava taşıtlarıyla ilgili aklınıza ne gelirse",
        "havacilik",
    ),
    Channel("yaşam", "hayatın içinden oluşlar, küçük detaylar", "yasam"),
    Channel("kripto", "dijital para dünyasına dair her şey", "kripto"),
]
