# Öğrenci: Esma Yıldırım
# tarih 11 10 2026
# closure, lambda ve bonus sure olcer

import time
from typing import Callable, Any


def hamle_sayaci() -> Callable[[], int]:
    """her cagrildiginda 1 artan bir sayac fonksiyonu dondurur (nonlocal)."""
    sayac = 0

    def say() -> int:
        nonlocal sayac
        sayac += 1
        return sayac

    return say


def en_bagli_gezegenler(galaksi: dict) -> list[str]:
    """gezegenleri baglanti sayisina gore azalan siralar.
    esitlikte alfabetik sira kullanir. sorted ve key=lambda ile."""
    baglantilar = galaksi["baglantilar"]
    return sorted(
        baglantilar,
        key=lambda g: (-len(baglantilar[g]), g),
    )


def sure_olc(fonksiyon: Callable) -> Callable:
    """fonksiyonun calisma suresini olcer.
    *args ve **kwargs ile cagiran bir sarmalayici dondurur."""
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        bas = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        gecen = time.perf_counter() - bas
        print(f"{fonksiyon.__name__} {gecen:.4f} saniye surdu")
        return sonuc
    return sarmalayici


if __name__ == "__main__":
    try:
        from uzay_oyunu.oyun import galaksi_kur
    except ModuleNotFoundError:
        from oyun import galaksi_kur

    # hamle sayaci denemesi
    sayac = hamle_sayaci()
    print("hamle 1:", sayac())
    print("hamle 2:", sayac())
    print("hamle 3:", sayac())
    print()

    # en_bagli_gezegenler denemesi
    g = galaksi_kur(
        ["dünya", "centauri", "sirius", "orion", "kara_delik"],
        {
            "dünya": ["centauri", "sirius"],
            "centauri": ["dünya", "sirius", "orion"],
            "sirius": ["centauri", "dünya", "orion", "kara_delik"],
            "orion": ["sirius", "centauri"],
            "kara_delik": ["sirius"],
        },
        "dünya",
        yakit=100,
    )
    print("en bagli gezegenler:", en_bagli_gezegenler(g))
    print()

    # bonus: sure_olc denemesi
    en_bagli_gezegenler = sure_olc(en_bagli_gezegenler)
    sonuc = en_bagli_gezegenler(g)
    print("sonuc:", sonuc)
