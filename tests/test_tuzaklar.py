# Öğrenci: Esma Yıldırım
# tarih 11 10 2026
# mutable default argument tuzagi testi

def yakit_ekle(miktar: int, depo: list[int] | None = None) -> list[int]:
    """depoya yakit ekler, none verilirse yeni liste olusturur"""
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo


def test_yakit_ekle_ayri_cagrilar():
    sonuc1 = yakit_ekle(10)
    sonuc2 = yakit_ekle(20)
    assert sonuc1 == [10]
    assert sonuc2 == [20]


def test_yakit_ekle_ucuncu():
    yakit_ekle(1)
    yakit_ekle(2)
    sonuc = yakit_ekle(3)
    assert sonuc == [3]


def test_yakit_ekle_mevcut_depo():
    depo = [5]
    sonuc = yakit_ekle(10, depo)
    assert sonuc == [5, 10]
    assert sonuc is depo


def test_yakit_ekle_bos_depo():
    sonuc = yakit_ekle(42, [])
    assert sonuc == [42]
