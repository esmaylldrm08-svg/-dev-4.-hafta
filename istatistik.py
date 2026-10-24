"""Kök modül yönlendiricisi: uzay_oyunu.istatistik fonksiyonlarını dışa aktarır.

Öğrenci: Esma Yıldırım
Ders: İleri Python Programlama - Hafta 4 Lab
"""

from uzay_oyunu.istatistik import (
    buyuk_harfli_gezegenler,
    buyuk_harfli_gezegenler_comp,
    buyuk_harfli_gezegenler_map,
    cok_baglantili_gezegenler,
    cok_baglantili_gezegenler_comp,
    cok_baglantili_gezegenler_filter,
    hizli_yolculuk,
    toplam_baglanti_sayisi,
    toplam_baglanti_sayisi_reduce,
    toplam_baglanti_sayisi_sum,
    yolculuk,
)

__all__ = [
    "buyuk_harfli_gezegenler",
    "buyuk_harfli_gezegenler_comp",
    "buyuk_harfli_gezegenler_map",
    "cok_baglantili_gezegenler",
    "cok_baglantili_gezegenler_comp",
    "cok_baglantili_gezegenler_filter",
    "hizli_yolculuk",
    "toplam_baglanti_sayisi",
    "toplam_baglanti_sayisi_reduce",
    "toplam_baglanti_sayisi_sum",
    "yolculuk",
]
