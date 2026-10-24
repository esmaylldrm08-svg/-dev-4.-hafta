"""Akış modülü (uzay_oyunu.akis) birim testleri.

Öğrenci: Esma Yıldırım
Ders: İleri Python Programlama - Hafta 4 Lab
"""

import itertools
import pytest
from uzay_oyunu.akis import fibonacci


# ============================================================================
# Görev 1 – Fibonacci Üreteci Testleri
# ============================================================================

def test_fibonacci_next_ilk_uc():
    """next() çağrıları ile Fibonacci dizisinin ilk 3 elemanını alma testi."""
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_ilk_oniki():
    """itertools.islice kullanarak ilk 12 Fibonacci sayısını alma testi."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(itertools.islice(fibonacci(), 12))
    assert sonuc == beklenen


def test_fibonacci_takewhile_yuzden_kucuk():
    """itertools.takewhile ile 100'den küçük Fibonacci sayılarını filtreleme testi."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(itertools.takewhile(lambda x: x < 100, fibonacci()))
    assert sonuc == beklenen


def test_fibonacci_tek_kullanimlik():
    """Üreteçlerin tek kullanımlık (exhaustible) durum nesneleri olduğunu doğrular.

    Aynı üreteç nesnesinden yapılan ardışık islice çağrıları farklı dilimler vermelidir.
    """
    g = fibonacci()
    ilk_bes = list(itertools.islice(g, 5))
    ikinci_bes = list(itertools.islice(g, 5))

    assert ilk_bes == [0, 1, 1, 2, 3]
    assert ikinci_bes == [5, 8, 13, 21, 34]
    assert ilk_bes != ikinci_bes


# ============================================================================
# Görev 2 – Yakıt Göstergesi Testleri
# ============================================================================

def test_yakit_gostergesi_ornek_cikti():
    """Ödev dokümanındaki list(yakit_gostergesi(100, 30)) beklenen çıktısını test eder."""
    from uzay_oyunu.akis import yakit_gostergesi

    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stop_iteration():
    """Yakıt tükendiğinde bir sonraki çağrıda StopIteration fırlatıldığını doğrular."""
    from uzay_oyunu.akis import yakit_gostergesi

    gosterge = yakit_gostergesi(20, 10)
    assert next(gosterge) == 10
    assert next(gosterge) == 0
    with pytest.raises(StopIteration):
        next(gosterge)


def test_yakit_gostergesi_sifir_baslangic():
    """Başlangıç yakıtı 0 veya negatifse hiçbir değer üretilmeden durmalıdır."""
    from uzay_oyunu.akis import yakit_gostergesi

    assert list(yakit_gostergesi(0, 10)) == []


def test_yakit_gostergesi_tek_adimda_tukenme():
    """Tüketim başlangıç yakıtından büyükse tek adımda 0 üretip sonlanmalıdır."""
    from uzay_oyunu.akis import yakit_gostergesi

    assert list(yakit_gostergesi(15, 25)) == [0]


# ============================================================================
# Görev 3 – Seyir Defteri Boru Hattı Testleri
# ============================================================================

def test_boru_hatti_toplam_yakit():
    """Ödev dokümanındaki boru hattı ile toplam yakıt hesabını (88) test eder."""
    from pathlib import Path
    from uzay_oyunu.akis import satirlari_oku, ayristir

    yol = Path(__file__).parent.parent / "veri" / "seyir.txt"
    toplam = sum(y for _, _, y in ayristir(satirlari_oku(str(yol))))
    assert toplam == 88


def test_boru_hatti_uzun_yolculuklar():
    """Ödev dokümanındaki yakıtı 10'dan büyük yolculukların hedeflerini test eder."""
    from pathlib import Path
    from uzay_oyunu.akis import satirlari_oku, ayristir, uzun_yolculuklar

    yol = Path(__file__).parent.parent / "veri" / "seyir.txt"
    kayitlar = ayristir(satirlari_oku(str(yol)))
    hedefler = [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_tembel_degerlendirme():
    """Boru hattının hiçbir adımda liste üretmeyip generator tipi döndürdüğünü doğrular."""
    import types
    from pathlib import Path
    from uzay_oyunu.akis import satirlari_oku, ayristir, uzun_yolculuklar

    yol = Path(__file__).parent.parent / "veri" / "seyir.txt"
    g_satir = satirlari_oku(str(yol))
    assert isinstance(g_satir, types.GeneratorType)

    g_ayristir = ayristir(g_satir)
    assert isinstance(g_ayristir, types.GeneratorType)

    g_uzun = uzun_yolculuklar(g_ayristir, 10)
    assert isinstance(g_uzun, types.GeneratorType)


# ============================================================================
# Görev 4 – Önbellekli Rota Sayacı Testleri
# ============================================================================

def test_rota_sayaci_ornek_galaksi():
    """Ödev dokümanındaki 10 bağlantılı referans galaksi çıktılarını test eder:
    say("dünya", 3) -> 9, say("dünya", 10) -> 2185, say("dünya", 40) -> 16832258606399
    """
    from uzay_oyunu.akis import rota_sayaci

    baglantilar = {
        "dünya": ["centauri", "sirius"],
        "centauri": ["dünya", "orion"],
        "sirius": ["dünya", "orion", "kara_delik"],
        "orion": ["centauri", "sirius"],
        "kara_delik": ["sirius"],
    }
    say = rota_sayaci(baglantilar)
    assert say("dünya", 3) == 9
    assert say("dünya", 10) == 2185
    assert say("dünya", 40) == 16832258606399


def test_rota_sayaci_galaksi_json():
    """Projedeki galaksi.json ile önbellekli rota sayacının çalıştığını ve cache_info ürettiğini doğrular."""
    import json
    from pathlib import Path
    from uzay_oyunu.akis import rota_sayaci

    yol = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(yol, encoding="utf-8") as f:
        galaksi = json.load(f)

    say = rota_sayaci(galaksi["baglantilar"])
    assert say("dünya", 0) == 1
    assert say("dünya", 3) == 16

    info = say.cache_info()
    assert info.hits > 0
    assert info.currsize > 0


# ============================================================================
# Görev 5 – map, filter, reduce ve functools.partial Testleri
# ============================================================================

@pytest.fixture
def ornek_galaksi_verisi():
    """Ödev dokümanındaki 10 bağlantılı referans galaksi verisi."""
    return {
        "gezegenler": ["dünya", "centauri", "sirius", "orion", "kara_delik"],
        "baglantilar": {
            "dünya": ["centauri", "sirius"],
            "centauri": ["dünya", "orion"],
            "sirius": ["dünya", "orion", "kara_delik"],
            "orion": ["centauri", "sirius"],
            "kara_delik": ["sirius"],
        },
    }


def test_buyuk_harfli_gezegenler_iki_yolla(ornek_galaksi_verisi):
    """Soru 1: map() ve liste üreteci ile büyük harf dönüşümünü test eder."""
    from uzay_oyunu.istatistik import (
        buyuk_harfli_gezegenler_comp,
        buyuk_harfli_gezegenler_map,
    )

    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    sonuc_map = buyuk_harfli_gezegenler_map(ornek_galaksi_verisi)
    sonuc_comp = buyuk_harfli_gezegenler_comp(ornek_galaksi_verisi)

    assert sonuc_map == beklenen
    assert sonuc_comp == beklenen
    assert sonuc_map == sonuc_comp


def test_cok_baglantili_gezegenler_iki_yolla(ornek_galaksi_verisi):
    """Soru 2: filter() ve liste üreteci ile en az iki bağlantılı gezegenleri test eder."""
    from uzay_oyunu.istatistik import (
        cok_baglantili_gezegenler_comp,
        cok_baglantili_gezegenler_filter,
    )

    beklenen = ["dünya", "centauri", "sirius", "orion"]
    sonuc_filter = cok_baglantili_gezegenler_filter(ornek_galaksi_verisi, 2)
    sonuc_comp = cok_baglantili_gezegenler_comp(ornek_galaksi_verisi, 2)

    assert sonuc_filter == beklenen
    assert sonuc_comp == beklenen
    assert sonuc_filter == sonuc_comp


def test_toplam_baglanti_sayisi_iki_yolla(ornek_galaksi_verisi):
    """Soru 3: reduce() ve sum() ile toplam bağlantı sayısını (10) test eder."""
    from uzay_oyunu.istatistik import (
        toplam_baglanti_sayisi_reduce,
        toplam_baglanti_sayisi_sum,
    )

    sonuc_reduce = toplam_baglanti_sayisi_reduce(ornek_galaksi_verisi)
    sonuc_sum = toplam_baglanti_sayisi_sum(ornek_galaksi_verisi)

    assert sonuc_reduce == 10
    assert sonuc_sum == 10
    assert sonuc_reduce == sonuc_sum


def test_hizli_yolculuk_partial():
    """functools.partial ile türetilen hizli_yolculuk fonksiyonunun davranışını test eder."""
    from uzay_oyunu.istatistik import hizli_yolculuk, yolculuk

    assert hizli_yolculuk.func == yolculuk
    assert hizli_yolculuk.keywords == {"hiz": 3.0}

    # mesafe 30 iken süre = 30 / 3 = 10.0 olmalı
    assert hizli_yolculuk(30) == 10.0
    assert hizli_yolculuk(9) == 3.0
    assert yolculuk(30, 3.0) == hizli_yolculuk(30)


# ============================================================================
# Bonus (+10) – Zamanlayıcı ve Meşgul Bekleme Testleri
# ============================================================================

def test_zamanlayici_aralik_dolunca_true():
    """zamanlayici üretecinin süre dolana kadar False, süre dolunca True ürettiğini test eder."""
    import time
    from uzay_oyunu.akis import zamanlayici

    g = zamanlayici(0.02)
    # Hemen çağrılınca henüz 0.02 saniye geçmediği için False olmalı
    assert next(g) is False

    # 0.025 saniye bekleyelim
    bas = time.perf_counter()
    while time.perf_counter() - bas < 0.025:
        pass

    # Süre dolduğunda True dönmeli
    assert next(g) is True


def test_tik_tak_programi_calisma():
    """tik_tak_programi fonksiyonunun başarıyla liste ürettiğini test eder (hızlı süre: 0.01s)."""
    from uzay_oyunu.akis import tik_tak_programi

    olaylar = tik_tak_programi(toplam_sure=0.01, yazdir=False)
    assert isinstance(olaylar, list)





