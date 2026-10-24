"""İstatistik modülü: map, filter, reduce ve functools.partial kullanımı.

Öğrenci: Esma Yıldırım
Ders: İleri Python Programlama - Hafta 4 Lab
"""

from functools import partial, reduce


# ============================================================================
# OKUNAKLILIK KARŞILAŞTIRMASI:
# Python'un tasarım felsefesine (Zen of Python - "Readability counts") göre;
# Liste üreteçleri (list comprehensions) ve yerleşik sum() fonksiyonu, map(),
# filter() ve reduce() fonksiyonlarına kıyasla çok daha açık, okunabilir ve
# Pythonic (Python'a özgü) bir yazım sunar.
#
# Nedenleri:
# 1. map() ve filter() genellikle isimsiz lambda fonksiyonlarına ihtiyaç duyar ve
#    çıktıyı doğrudan görmek için list(...) ile sarmalanmaları gerekir. Bu da görsel
#    gürültüye ve gereksiz parantez yığınına sebep olur.
# 2. Liste üreteçleri ise doğrudan matematiksel küme notasyonuna ([ifade for öge in liste if koşul])
#    dayanır; filtreleme ve dönüştürme işlemleri tek bir satırda doğal dille okunabilir.
# 3. reduce() akışları karmaşıklaştırabildiği ve tek bakışta anlaşılmasını zorlaştırdığı
#    için Python 3'te yerleşik (built-in) fonksiyonlar arasından çıkarılarak functools
#    kütüphanesine taşınmıştır. Onun yerine sum() veya açık döngüler tavsiye edilir.
# ============================================================================


# ----------------------------------------------------------------------------
# Soru 1: Gezegen adlarının büyük harfli listesi
# ----------------------------------------------------------------------------

def buyuk_harfli_gezegenler_map(galaksi: dict) -> list[str]:
    """map() fonksiyonu kullanarak gezegen adlarını büyük harfe dönüştürür.

    Args:
        galaksi: Gezegen listesi ve bağlantıları içeren sözlük.

    Returns:
        list[str]: Büyük harflerle yazılmış gezegen adları listesi.
    """
    return list(map(str.upper, galaksi["gezegenler"]))


def buyuk_harfli_gezegenler_comp(galaksi: dict) -> list[str]:
    """Liste üreteci (list comprehension) ile gezegen adlarını büyük harfe dönüştürür.

    Args:
        galaksi: Gezegen listesi ve bağlantıları içeren sözlük.

    Returns:
        list[str]: Büyük harflerle yazılmış gezegen adları listesi.
    """
    return [g.upper() for g in galaksi["gezegenler"]]


def buyuk_harfli_gezegenler(galaksi: dict) -> list[str]:
    """Gezegen adlarının büyük harfli listesini döndürür."""
    return buyuk_harfli_gezegenler_comp(galaksi)


# ----------------------------------------------------------------------------
# Soru 2: En az iki bağlantısı olan gezegenler
# ----------------------------------------------------------------------------

def cok_baglantili_gezegenler_filter(galaksi: dict, min_baglanti: int = 2) -> list[str]:
    """filter() fonksiyonu ile en az min_baglanti kadar komşusu olan gezegenleri süzer.

    Args:
        galaksi: Galaksi verisi sözlüğü.
        min_baglanti: Asgari bağlantı sayısı (varsayılan 2).

    Returns:
        list[str]: Koşulu sağlayan gezegenlerin adları.
    """
    baglantilar = galaksi["baglantilar"]
    return list(
        filter(
            lambda g: len(baglantilar.get(g, [])) >= min_baglanti,
            galaksi["gezegenler"],
        )
    )


def cok_baglantili_gezegenler_comp(galaksi: dict, min_baglanti: int = 2) -> list[str]:
    """Liste üreteci ile en az min_baglanti kadar komşusu olan gezegenleri süzer.

    Args:
        galaksi: Galaksi verisi sözlüğü.
        min_baglanti: Asgari bağlantı sayısı (varsayılan 2).

    Returns:
        list[str]: Koşulu sağlayan gezegenlerin adları.
    """
    baglantilar = galaksi["baglantilar"]
    return [
        g
        for g in galaksi["gezegenler"]
        if len(baglantilar.get(g, [])) >= min_baglanti
    ]


def cok_baglantili_gezegenler(galaksi: dict, min_baglanti: int = 2) -> list[str]:
    """En az iki bağlantısı olan gezegenleri döndürür."""
    return cok_baglantili_gezegenler_comp(galaksi, min_baglanti)


# ----------------------------------------------------------------------------
# Soru 3: Toplam bağlantı sayısı
# ----------------------------------------------------------------------------

def toplam_baglanti_sayisi_reduce(galaksi: dict) -> int:
    """functools.reduce() kullanarak haritadaki toplam bağlantı sayısını hesaplar.

    Args:
        galaksi: Galaksi verisi sözlüğü.

    Returns:
        int: Toplam bağlantı (komşuluk) sayısı.
    """
    baglantilar = galaksi["baglantilar"]
    return reduce(
        lambda toplam, komsular: toplam + len(komsular),
        baglantilar.values(),
        0,
    )


def toplam_baglanti_sayisi_sum(galaksi: dict) -> int:
    """sum() fonksiyonu ve üreteç ifadesi ile haritadaki toplam bağlantı sayısını hesaplar.

    Args:
        galaksi: Galaksi verisi sözlüğü.

    Returns:
        int: Toplam bağlantı sayısı.
    """
    baglantilar = galaksi["baglantilar"]
    return sum(len(komsular) for komsular in baglantilar.values())


def toplam_baglanti_sayisi(galaksi: dict) -> int:
    """Toplam bağlantı sayısını döndürür."""
    return toplam_baglanti_sayisi_sum(galaksi)


# ----------------------------------------------------------------------------
# Yolculuk fonksiyonu ve functools.partial ile hizli_yolculuk
# ----------------------------------------------------------------------------

def yolculuk(mesafe: float, hiz: float = 1.0) -> float:
    """Verilen mesafe ve hıza göre seyahat süresini (sure = mesafe / hiz) hesaplar.

    Args:
        mesafe: Seyahat edilecek birim mesafe.
        hiz: Seyahat hızı (varsayılan 1.0).

    Returns:
        float: Yolculuk için gereken süre.
    """
    return mesafe / hiz


# functools.partial ile 'hiz' parametresi 3.0 olarak sabitlenmiş hızlı yolculuk fonksiyonu
hizli_yolculuk = partial(yolculuk, hiz=3.0)
