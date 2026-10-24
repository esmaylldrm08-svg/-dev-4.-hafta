# İleri Python Programlama – Hafta 4 Lab Ödevi: Üreteçler ve functools

**Öğrenci Adı Soyadı:** Esma Yıldırım  
**Öğrenci Numarası:** *(20253004004)*  
**Ders:** İleri Python Programlama  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  

---

## Proje Hakkında
Bu çalışma, önceki haftalarda geliştirilen **Uzay Macerası** projesine şu ileri Python yeteneklerini kazandırır:
1. **Üreteçler (Generators):** `yield` ifadesi ile sonsuz diziler (`fibonacci`), durum koruyan yakıt göstergeleri (`yakit_gostergesi`) ve zamanlayıcılar (`zamanlayici`).
2. **Veri Boru Hattı (Data Processing Pipeline):** Seyir defteri verisini dosyadan satır satır okuyan, ayrıştıran ve süzgeçten geçiren; hiçbir aşamada tüm dosyayı belleğe almayan (tembel değerlendirme / lazy evaluation) üç aşamalı akış.
3. **Önbellekleme (`@lru_cache`):** Özyinelemeli (recursive) rota hesabı üzerinde dinamik programlama ve memoization uygulayarak üstel zaman karmaşıklığını ($O(b^n)$) doğrusal zamana ($O(V \cdot n)$) indiren rota sayacı.
4. **Fonksiyonel Programlama:** `map`, `filter`, `reduce`, yerleşik fonksiyonlar (`sum`), liste üreteçleri (list comprehensions) ve `functools.partial` ile fonksiyon özelleştirme.
5. **Meşgul Bekleme (Busy Waiting) vs Sistem Uykusu (`time.sleep`):** İşlemci döngüleri ve işletim sistemi iş parçacığı durumları analizi.

---

## Görev 4 – Önbellekli Rota Sayacı Performans Ölçümleri

`rota_sayaci(baglantilar)` fonksiyonu, içinde `@lru_cache(maxsize=None)` ile süslenmiş özyinelemeli `rota_sayisi(gezegen, adim)` fonksiyonunu döndürür. Verilen bir gezegenden başlayarak tam `adim` uzunluğundaki tüm olası farklı yolculuk rotalarının sayısını hesaplar.

`time.perf_counter()` ile `adim=20` için yapılan önbelleksiz ve önbellekli performans ölçüm sonuçları:

### 1. Referans Galaksi Haritası (10 Bağlantılı Örnek Galaksi)
* `dünya`: `['centauri', 'sirius']`
* `centauri`: `['dünya', 'orion']`
* `sirius`: `['dünya', 'orion', 'kara_delik']`
* `orion`: `['centauri', 'sirius']`
* `kara_delik`: `['sirius']`

* **Hesaplanan Rota Sayısı (`adim=20`):** `4.315.343`
* **Önbelleksiz Sürüm Süresi:** `0.721026 saniye`
* **Önbellekli Sürüm Süresi:** `0.000027 saniye`
* **Hızlanma Oranı:** Yaklaşık **26.745 kat** daha hızlı!
* **`cache_info()` Çıktısı:** `CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)`

---

### 2. Projedeki `galaksi.json` Haritası
* `dünya`: `['centauri', 'sirius']`
* `centauri`: `['dünya', 'sirius', 'orion']`
* `sirius`: `['centauri', 'dünya', 'orion', 'kara_delik']`
* `orion`: `['sirius', 'centauri']`
* `kara_delik`: `['sirius']`

* **Hesaplanan Rota Sayısı (`adim=20`):** `336.745.984`
* **Önbellekli Sürüm Süresi:** `0.000036 saniye`
* **`cache_info()` Çıktısı:** `CacheInfo(hits=128, misses=98, maxsize=None, currsize=98)`

### Teorik Değerlendirme
Önbelleksiz özyinelemede dallanma faktörü ($b \approx 2-3$) nedeniyle işlem karmaşıklığı $O(b^{\text{adim}})$ mertebesinde üstel olarak büyür. `adim=20` için milyonlarca fonksiyon çağrısı tekrar tekrar çalışır.  
`@lru_cache` sayesinde daha önce ziyaret edilen `(gezegen, kalan_adim)` alt problem durumları hafızada önbelleğe alınır. Aynı alt problem ikinci kez çağrıldığında doğrudan $O(1)$ sürede bellekten getirilir. Bu sayede genel zaman karmaşıklığı durum uzayı büyüklüğü olan $O(|V| \times \text{adim})$ mertebesine (doğrusal zamana) iner.

---

## Görev 5 – Okunaklılık Karşılaştırması (`map/filter/reduce` vs Liste Üreteçleri)

Python'un tasarım felsefesi (The Zen of Python - PEP 20) *"Readability counts"* (Okunabilirlik önemlidir) ve *"Simple is better than complex"* ilkelerini temel alır.

1. **`map` ve `filter`:**
   * Genellikle `lambda` ifadelerine ihtiyaç duyarlar.
   * Dönen sonuçlar birer iterator (üreteç) olduğu için doğrudan liste elde etmek adına `list(...)` ile sarmalanmaları gerekir. Bu durum parantez karmaşasına ve görsel gürültüye yol açar.
2. **`reduce`:**
   * Akümülatör ve eleman ilişkisi karmaşıklaştıkça kodun tek bakışta anlaşılmasını zorlaştırır.
   * Bu okunabilirlik dezavantajı nedeniyle Python 3'te yerleşik fonksiyonlar arasından çıkarılıp `functools` modülüne taşınmıştır.
3. **Liste Üreteçleri (List Comprehensions) ve `sum()`:**
   * Matematikteki küme gösterimine benzer bir söz dizimine sahiptir: `[ifade for oge in koleksiyon if kosul]`.
   * Ne yapıldığı (dönüşüm, filtreleme) soldan sağa doğal dille okunabilir.
   * Bu nedenle Python topluluğunda liste üreteçleri ve yerleşik `sum()` fonksiyonu çok daha **okunaklı, temiz ve Pythonic** kabul edilir.

---

## Bonus (+10 Puan) – Meşgul Bekleme (Busy Waiting) ve `time.sleep` Farkı

`tik_tak_programi`, `zamanlayici(aralik)` üretecini kullanarak 10 saniye boyunca her 2 saniyede "tik", her 5 saniyede "tak" yazdırır.

### Neden "Meşgul Bekleme" (Busy Waiting)?
Bu programda zamanın dolup dolmadığı, CPU'nun kesintisiz bir `while True` döngüsü içinde sürekli olarak `time.perf_counter()` değerini sorgulaması (polling) ile kontrol edilir. İşlemci bu süreçte hiçbir zaman boşta kalmaz; çekirdek sürekli döngü komutlarını çalıştırarak **%100 CPU kullanımına**, aşırı ısınmaya ve gereksiz enerji tüketimine yol açar.

### `time.sleep()` ile Farkı:
1. **İşletim Sistemi Seviyesinde Durum:**
   * `time.sleep(sure)` çağrıldığında, Python süreci işletim sistemi çekirdeğine (OS kernel) bir sistem çağrısı (nanosleep / syscall) yapar.
   * İşletim sistemi bu iş parçacığını (thread) **UYKU / BEKLEME (BLOCKED)** durumuna geçirir ve CPU zamanlayıcısı bu çekirdeği diğer çalışan işlemlere devreder.
   * Süre dolana kadar işlemci bu iş parçacığı için **%0 CPU harcar**. Süre dolduğunda donanım zamanlayıcı kesmesi (timer interrupt) ile iş parçacığı tekrar **HAZIR (READY)** durumuna getirilir.
2. **Kullanım Alanları:**
   * **`time.sleep()`**: Standart gecikmeler, arka plan görevleri ve enerji verimliliği için tercih edilir.
   * **Meşgul Bekleme (Busy Waiting)**: Ancak donanım seviyesinde mikrosaniyelik/nanosaniyelik ultra düşük gecikme gereken durumlarda (işletim sistemi bağlam değişim [context switch] maliyetini ortadan kaldırmak için) veya kütüphanelerin işbirlikçi döngülerinde (cooperative multitasking) kullanılır.

---

## Testleri Çalıştırma

Tüm testleri (41 adet eski ve yeni test) çalıştırmak için:

```bash
uv run pytest
```

Örnek test çıktısı:
```text
collected 41 items

tests/test_akis.py ...................                                   [ 46%]
tests/test_fonksiyonlar.py ..................                            [ 90%]
tests/test_tuzaklar.py ....                                              [100%]

============================== 41 passed in 0.06s ==============================
```
