# Görev 4b - Kapsam Örnekleri
# Öğrenci: Esma Yıldırım

## Örnek 1 - Yerel kapsam

```python
x = 10
def f():
    x = 20
    print(x)
f()
print(x)
```

**Tahminim:** 20 sonra 10

**Gerçek sonuç:** 20 sonra 10

**Neden:** fonksiyonun icinde x = 20 yazmak yeni bir yerel degisken olusturuyor, distaki x'i degistirmiyor. f() kendi x'ini (20) yazdirir, distaki print ise global x'i (10) yazdirir.

---

## Örnek 2 - global kullanımı

```python
x = 10
def f():
    global x
    x = 20
f()
print(x)
```

**Tahminim:** 20

**Gerçek sonuç:** 20

**Neden:** global x deyince fonksiyondaki x artik global olan x oluyor. x = 20 global degeri degistirdigi icin print(x) de 20 yaziyor.

---

## Örnek 3 - UnboundLocalError

```python
x = 10
def f():
    print(x)
    x = 20
f()
```

**Tahminim:** 10 yazdirir sonra x = 20 yapar

**Gerçek sonuç:** UnboundLocalError hatasi veriyor

**Neden:** python fonksiyonu derlerken x = 20 satirini gorunce x'i yerel degisken olarak isaretliyor. ama print(x) satiri x'e deger atanmadan once calistigi icin hata veriyor. python once atama yapilmasini bekliyor ama biz okumaya calisiyoruz, bu yuzden UnboundLocalError firlatiliyor.

bunu cozmek icin nonlocal kullanilabilir (ic ice fonksiyonlarda) ya da global kullanilabilir ama odevde global yasak.
