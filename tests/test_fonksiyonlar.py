# Öğrenci: Esma Yıldırım
# tarih 11 10 2026
# saf fonksiyonlar ve galaksi_kur testleri

import json
from pathlib import Path
import pytest
from uzay_oyunu.oyun import envanter_metni, galaksi_kur, hedef_menusu


# envanter_metni testleri

def test_envanter_hepsi_var():
    sonuc = envanter_metni(True, True, True)
    assert sonuc == "Sende: bol kredi, güçlü motorlar, yetenekli bir pilot"


def test_envanter_bos():
    assert envanter_metni(False, False, False) == ""


def test_envanter_kredi_ve_pilot():
    assert envanter_metni(True, False, True) == "Sende: bol kredi, yetenekli bir pilot"


def test_envanter_sadece_motor():
    assert envanter_metni(False, True, False) == "Sende: güçlü motorlar"


def test_envanter_sadece_kredi():
    assert envanter_metni(True, False, False) == "Sende: bol kredi"


def test_envanter_sadece_pilot():
    assert envanter_metni(False, False, True) == "Sende: yetenekli bir pilot"


def test_envanter_str_donuyor():
    # saf fonksiyon oldugu icin print degil str donmeli
    sonuc = envanter_metni(True, True, True)
    assert isinstance(sonuc, str)


# hedef_menusu testleri

def test_hedef_tek():
    sonuc = hedef_menusu(["centauri"])
    assert "Nereye gitmek istersin?" in sonuc
    assert "[1] centauri" in sonuc


def test_hedef_iki():
    sonuc = hedef_menusu(["centauri", "sirius"])
    satirlar = sonuc.split("\n")
    assert satirlar[0] == "Nereye gitmek istersin?"
    assert satirlar[1] == "[1] centauri"
    assert satirlar[2] == "[2] sirius"


def test_hedef_bos():
    sonuc = hedef_menusu([])
    assert sonuc == "Nereye gitmek istersin?"


def test_hedef_uc_tane():
    sonuc = hedef_menusu(["a", "b", "c"])
    assert "[1] a" in sonuc
    assert "[2] b" in sonuc
    assert "[3] c" in sonuc


# galaksi_kur testleri

def test_galaksi_temel():
    g = galaksi_kur(
        ["dünya", "mars"],
        {"dünya": ["mars"], "mars": ["dünya"]},
        "dünya",
        yakit=100,
    )
    assert g["konum"] == "dünya"
    assert g["yakit"] == 100
    assert "mars" in g["baglantilar"]["dünya"]


def test_galaksi_varsayilan_yakit():
    # yakit verilmezse 50 olmali
    g = galaksi_kur(["mars"], {"mars": []}, "mars")
    assert g["yakit"] == 50


def test_galaksi_yanlis_baslangic():
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "plüton")


def test_galaksi_json_yukle():
    yol = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    g = galaksi_kur(**veri)
    assert g["konum"] == "dünya"
    assert g["yakit"] == 100


def test_baglantilar_sirasi():
    # sira korunmali yoksa eski testler bozulur
    yol = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    g = galaksi_kur(**veri)
    assert g["baglantilar"]["dünya"] == ["centauri", "sirius"]
    assert g["baglantilar"]["sirius"] == ["centauri", "dünya", "orion", "kara_delik"]


# gorev 5 - hamle_sayaci ve en_bagli_gezegenler testleri

def test_hamle_sayaci():
    from uzay_oyunu.araclar import hamle_sayaci
    sayac = hamle_sayaci()
    assert sayac() == 1
    assert sayac() == 2
    assert sayac() == 3


def test_en_bagli_gezegenler():
    from uzay_oyunu.araclar import en_bagli_gezegenler
    yol = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    g = galaksi_kur(**veri)
    assert en_bagli_gezegenler(g) == ["sirius", "centauri", "dünya", "orion", "kara_delik"]

