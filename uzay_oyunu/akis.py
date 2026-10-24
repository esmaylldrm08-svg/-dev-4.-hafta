"""Uzay oyunu akış modülü: Üreteçler, veri işleme boru hattı ve önbellekli rota hesabı.

Öğrenci: Esma Yıldırım
Ders: İleri Python Programlama - Hafta 4 Lab
"""

from collections.abc import Generator
import itertools


def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreten üreteç (generator) fonksiyonu.

    İlk iki terimi 0 ve 1'dir. Her iterasyonda bir sonraki Fibonacci sayısını yield eder.

    Yields:
        int: Sıradaki Fibonacci sayısı.

    Örnek:
        >>> g = fibonacci()
        >>> (next(g), next(g), next(g))
        (0, 1, 1)
    """
    a: int = 0
    b: int = 1
    while True:
        yield a
        a, b = b, a + b


def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tüketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'ın altına düşemez (en az 0 olur). Kalan yakıt 0'a ulaştığında son değer
    olarak 0 üretilir ve ardından üreteç sonlanır (StopIteration fırlatır).

    Args:
        yakit: Başlangıç yakıt miktarı.
        tuketim: Her seyahatte harcanan yakıt miktarı.

    Yields:
        int: Seyahat sonrası kalan güncel yakıt miktarı.

    Örnek:
        >>> list(yakit_gostergesi(100, 30))
        [70, 40, 10, 0]
    """
    kalan: int = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan


# ============================================================================
# Görev 3 – Seyir Defteri Boru Hattı (Data Processing Pipeline)
# ============================================================================

def satirlari_oku(yol: str) -> Generator[str, None, None]:
    """Seyir defteri dosyasını satır satır okuyarak boş ve yorum satırlarını süzen üreteç.

    Tembel değerlendirme (lazy evaluation) uygular; tüm dosyayı tek seferde belleğe
    yüklemez (list/readlines kullanılmaz).

    Args:
        yol: Okunacak metin dosyasının yolu.

    Yields:
        str: Başındaki ve sonundaki boşlukları temizlenmiş geçerli satır metni.
    """
    with open(yol, mode="r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if not temiz or temiz.startswith("#"):
                continue
            yield temiz


def ayristir(
    satirlar: Generator[str, None, None],
) -> Generator[tuple[str, str, int], None, None]:
    """Seyir satırlarını ayrıştırıp (kaynak, hedef, yakit) demetleri üreten üreteç.

    'kaynak -> hedef yakit' biçimindeki satırları çözümler.

    Args:
        satirlar: Satır metinlerini üreten bir üreteç veya yinelenebilir nesne.

    Yields:
        tuple[str, str, int]: (kaynak_gezegeni, hedef_gezegeni, harcanan_yakit) demeti.
    """
    for satir in satirlar:
        sol, sag = satir.split("->")
        kaynak = sol.strip()
        hedef, yakit_str = sag.strip().rsplit(maxsplit=1)
        yield (kaynak, hedef, int(yakit_str))


def uzun_yolculuklar(
    kayitlar: Generator[tuple[str, str, int], None, None],
    esik: int,
) -> Generator[tuple[str, str, int], None, None]:
    """Yakıt tüketimi verilen eşik değerinden büyük olan yolculukları süzen üreteç.

    Boru hattı boyunca veriyi akış (stream) halinde filtreler, liste oluşturmaz.

    Args:
        kayitlar: (kaynak, hedef, yakit) demeti üreten üreteç.
        esik: Minimum yakıt eşiği (yakit > esik şartı aranır).

    Yields:
        tuple[str, str, int]: Eşiği geçen yolculuk kaydı.
    """
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit


# ============================================================================
# Görev 4 – Önbellekli Rota Sayacı (Memoization with @lru_cache)
# ============================================================================

def rota_sayaci(baglantilar: dict[str, list[str]]):
    """Verilen bağlantı haritası üzerinde rota sayımı yapan önbellekli fonksiyon döndürür.

    İçinde @lru_cache ile süslenmiş özyinelemeli rota_sayisi(gezegen, adim)
    fonksiyonunu tanımlayıp döndürür (closure deseni).

    Args:
        baglantilar: Gezegenlerin komşuluk bağlantılarını tutan sözlük.

    Returns:
        Callable[[str, int], int]: Önbellekli rota_sayisi fonksiyonu.

    Örnek:
        >>> say = rota_sayaci(galaksi["baglantilar"])
        >>> say("dünya", 3)
        9
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Verilen gezegenden başlayıp tam adim kadar sıçrayan farklı rota sayısını hesaplar.

        Args:
            gezegen: Başlangıç gezegeni.
            adim: Atılacak tam adım sayısı.

        Returns:
            int: Farklı rotaların toplam sayısı.
        """
        if adim == 0:
            return 1
        komsular = baglantilar.get(gezegen, [])
        return sum(rota_sayisi(komsu, adim - 1) for komsu in komsular)

    return rota_sayisi


# ============================================================================
# Bonus (+10) – Zamanlayıcı Üreteci ve Meşgul Bekleme (Busy Waiting)
# ============================================================================

def zamanlayici(aralik: float) -> Generator[bool, None, None]:
    """Verilen zaman aralığı dolduğunda True, dolmadığında False üreten üreteç.

    Meşgul bekleme (busy waiting) prensibiyle çalışır: her çağrıda saati sorgular
    ve aralık aşıldığında True üreterek yeni hedef zamanı belirler.

    Args:
        aralik: Saniye cinsinden tetiklenme periyodu.

    Yields:
        bool: Aralık tamamlandıysa True, henüz tamamlanmadıysa False.
    """
    import time

    hedef: float = time.perf_counter() + aralik
    while True:
        simdi: float = time.perf_counter()
        if simdi >= hedef:
            hedef += aralik
            yield True
        else:
            yield False


def tik_tak_programi(
    toplam_sure: float = 10.0, yazdir: bool = True
) -> list[tuple[float, str]]:
    """10 saniye boyunca her 2 saniyede 'tik', her 5 saniyede 'tak' yazdıran program.

    zamanlayici üretecini kullanarak meşgul bekleme döngüsü içinde olayları tetikler.

    Args:
        toplam_sure: Programın toplam çalışma süresi (varsayılan 10 saniye).
        yazdir: Konsola anlık çıktı basılıp basılmayacağı.

    Returns:
        list[tuple[float, str]]: (geçen_süre, mesaj) olay listesi.
    """
    import time

    tik = zamanlayici(2.0)
    tak = zamanlayici(5.0)

    olaylar: list[tuple[float, str]] = []
    baslangic = time.perf_counter()

    while (time.perf_counter() - baslangic) <= toplam_sure:
        gecen = time.perf_counter() - baslangic
        if next(tik):
            olaylar.append((round(gecen, 2), "tik"))
            if yazdir:
                print(f"[{gecen:.2f}s] tik")
        if next(tak):
            olaylar.append((round(gecen, 2), "tak"))
            if yazdir:
                print(f"[{gecen:.2f}s] tak")

    return olaylar




