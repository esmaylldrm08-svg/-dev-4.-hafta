# Öğrenci: Esma Yıldırım
# tarih 11 10 2026
# gorev kayit modulu - esnek parametreler


def gorev_kaydi(baslik: str, *adimlar: str, oncelik: str = "normal",
                **ekler: str) -> None:
    """gorevi formatli sekilde yazdirir.
    oncelik sadece keyword olarak verilebilir."""
    print(f"[{oncelik.upper()}] {baslik}")
    for i, adim in enumerate(adimlar, 1):
        print(f"  {i}. {adim}")
    for anahtar, deger in ekler.items():
        print(f"  {anahtar}: {deger}")


if __name__ == "__main__":
    # cagri bicimi 1 - listeyi acarak ve sozlugu acarak
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ekstra = {"sorumlu": "Ayse"}
    gorev_kaydi("Kara deliğe atla", *adimlar, oncelik="yüksek", **ekstra)

    print()

    # cagri bicimi 2 - dogrudan argümanlarla
    gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan", "Pilot bul", "Hiperdrive al",
        oncelik="yüksek",
        sorumlu="Ayse",
    )
