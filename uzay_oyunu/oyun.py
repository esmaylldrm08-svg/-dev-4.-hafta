# Öğrenci: Esma Yıldırım
# tarih 11 10 2026
# uzay oyunu ana modul - saf fonksiyonlar, galaksi_kur ve travel

import json
from pathlib import Path


def galaksi_kur(gezegenler: list[str], baglantilar: dict[str, list[str]],
                baslangic: str, **kwargs) -> dict:
    """galaksi verisini sozluk olarak olusturur.
    baslangic listede yoksa ValueError firlatir.
    yakit verilmezse varsayilan 50."""
    if baslangic not in gezegenler:
        raise ValueError(f"'{baslangic}' gezegeni listede yok")
    yakit = kwargs.get("yakit", 50)
    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": yakit,
    }


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """envanterdeki ogeleri metin olarak dondurur.
    hicbir oge yoksa bos metin doner. print cagirmaz."""
    ogeler = []
    if credits:
        ogeler.append("bol kredi")
    if engines:
        ogeler.append("güçlü motorlar")
    if copilot:
        ogeler.append("yetenekli bir pilot")
    if not ogeler:
        return ""
    return "Sende: " + ", ".join(ogeler)


def hedef_menusu(hedefler: list[str]) -> str:
    """numarali hedef menusu dondurur. print cagirmaz."""
    satirlar = ["Nereye gitmek istersin?"]
    for i, hedef in enumerate(hedefler, 1):
        satirlar.append(f"[{i}] {hedef}")
    return "\n".join(satirlar)


def travel() -> None:
    """uzay oyununun ana dongusu.
    galaksi.json dosyasindan veri yukler ve oyunu baslatir."""
    try:
        from uzay_oyunu.araclar import hamle_sayaci
    except ModuleNotFoundError:
        from araclar import hamle_sayaci

    try:
        from uzay_oyunu.akis import yakit_gostergesi
    except ModuleNotFoundError:
        from akis import yakit_gostergesi

    # galaksi verisini json dosyasindan yukle
    veri_yolu = Path(__file__).parent / "galaksi.json"
    with open(veri_yolu, encoding="utf-8") as f:
        veri = json.load(f)

    galaksi = galaksi_kur(**veri)
    gosterge = yakit_gostergesi(galaksi["yakit"], 5)

    # oyun durumu
    credits = False
    engines = False
    copilot = False
    sayac = hamle_sayaci()
    toplam_hamle = 0

    print("=" * 40)
    print("        UZAY MACERASI")
    print("=" * 40)
    print(f"\nHos geldin kasif! '{galaksi['konum']}' gezegenindsin.")
    print(f"Yakitin: {galaksi['yakit']}")
    print("Hedefin: kara_delik'e ulasmak!\n")

    while True:
        planet = galaksi["konum"]

        # gezegene ozel olaylar
        if planet == "centauri" and not credits:
            credits = True
            print("Centauri'de hazine buldun! Bol kredin var.")
        elif planet == "orion" and not engines:
            engines = True
            print("Orion'da guclu motorlar buldun!")
        elif planet == "sirius" and not copilot:
            copilot = True
            print("Sirius'ta yetenekli bir pilot sana katildi!")
        elif planet == "kara_delik":
            print(f"\nKara delige ulastin! Tebrikler!")
            print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
            break

        # envanteri goster
        envanter = envanter_metni(credits, engines, copilot)
        if envanter:
            print(envanter)

        # yakit kontrolu
        if galaksi["yakit"] <= 0:
            print("\nYakıtın bitti, uzayda sürükleniyorsun...")
            print(f"Toplam {toplam_hamle} hamle yaptin.")
            break

        print(f"\nKonum: {planet} | Yakit: {galaksi['yakit']}")

        # hedefleri goster - baglantilar uzerinden
        hedefler = galaksi["baglantilar"][planet]
        print(hedef_menusu(hedefler))

        # kullanici secimi
        try:
            secim = int(input("Secimin (numara): ")) - 1
        except (ValueError, EOFError):
            print("Gecersiz giris, tekrar dene.")
            continue

        if not (0 <= secim < len(hedefler)):
            print("Gecersiz secim, tekrar dene.")
            continue

        yeni_gezegen = hedefler[secim]
        galaksi["konum"] = yeni_gezegen
        try:
            galaksi["yakit"] = next(gosterge)
        except StopIteration:
            print("\nYakıtın bitti, uzayda sürükleniyorsun...")
            print(f"Toplam {toplam_hamle} hamle yaptin.")
            break
        toplam_hamle = sayac()

        print(f"\n{planet} -> {yeni_gezegen} yolculugu...")


if __name__ == "__main__":
    travel()
