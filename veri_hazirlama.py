# Pandas kütüphanesini içe aktarıyorum.
# CSV okuma ve tablo işlemleri için kullanıyorum.
import pandas as pd

# re kütüphanesini içe aktarıyorum.
# "regular expressions" — metin içinde örüntü aramak ve temizlemek için kullanılır.
# Şu an aktif kullanmıyorum ama ileride noktalama temizleme gibi
# işlemler eklemek istediğimde hazır olsun diye import ettim.
import re


# CSV dosyasını okuyup pandas tablosuna (DataFrame) çeviren fonksiyonu tanımlıyorum.
# dosya_yolu → okunacak CSV dosyasının yolu, örn: 'data/yorumlar.csv'
def veri_yukle(dosya_yolu):
    df = pd.read_csv(dosya_yolu, encoding='cp1254')
    # encoding='cp1254' → Windows'un Türkçe için kullandığı karakter seti.
    # Bunu belirtmezsem ş, ğ, ü gibi harflerde hata alırım.
    return df
# NOT: Bu fonksiyon aşağıda daha gelişmiş haliyle tekrar tanımlandı.
# Python'da aynı isimde iki fonksiyon olursa alttaki geçerli olur,
# üstteki ezilir. Bu bir refaktör sürecinin izini — geliştirirken
# önce basit yazdım, sonra encoding parametresi ekledim.


# Tabloyu temizleyen fonksiyonu tanımlıyorum.
# df → içinde 'yorum' sütunu olan pandas tablosu
def veri_temizle(df):

    # 'yorum' sütununda değeri olmayan (NaN/boş) satırları siliyorum.
    # dropna() → "drop not available" yani eksik veriyi at demek.
    # subset=['yorum'] → sadece yorum sütununa bakıyorum,
    # başka sütunlarda boşluk varsa o satırı silmiyorum.
    df = df.dropna(subset=['yorum'])

    # Her yorumun başındaki ve sonundaki boşluk karakterlerini temizliyorum.
    # Örneğin "  harika ürün  " → "harika ürün" oluyor.
    # str.strip() → pandas'ta metin sütunlarına toplu işlem yapmamı sağlıyor.
    df['yorum'] = df['yorum'].str.strip()

    # Strip sonrası tamamen boş kalan satırları siliyorum.
    # Örneğin yorum sütununda sadece boşluk olan satırlar
    # strip() sonrası "" oluyor — bunları da atıyorum.
    df = df[df['yorum'] != '']

    # Aynı yorumu birden fazla kez içeren satırları siliyorum.
    # Aynı yorum iki kez analiz edilirse sonuçlar çarpıtılır.
    # subset=['yorum'] → sadece yorum sütununa göre kontrol ediyorum.
    df = df.drop_duplicates(subset=['yorum'])

    # Satırları sildikten sonra index numaraları karışık kalıyor.
    # Örneğin 0, 1, 3, 5, 7 gibi — aralarda boşluklar oluşuyor.
    # reset_index(drop=True) ile 0'dan başlayarak yeniden numaralandırıyorum.
    # drop=True → eski index'i sütun olarak ekleme, tamamen sıfırla demek.
    df = df.reset_index(drop=True)
    return df
# Fonksiyonun geliştirilmiş hali — encoding parametresi eklendi.
# encoding='cp1254' varsayılan değer olarak atandı.
# Yani ben encoding belirtmezsem otomatik cp1254 kullanıyor,
# ama istersem farklı bir encoding de verebiliyorum — esnek hale geldi.
# Bu fonksiyon üstteki veri_yukle'nin üzerine yazıyor, o artık geçersiz.
def veri_yukle(dosya_yolu, encoding='cp1254'):
    df = pd.read_csv(dosya_yolu, encoding=encoding)
    return df


# Bu blok sadece bu dosyayı doğrudan çalıştırdığımda devreye giriyor.
# Başka bir dosyadan import edildiğinde bu kısım çalışmıyor.
# Yani bu benim "her şey çalışıyor mu?" diye kontrol ettiğim test alanım.
if __name__ == '__main__':
    # CSV dosyamı okuyorum — encoding belirtmiyorum çünkü
    # fonksiyonun varsayılan değeri zaten cp1254.
    df = veri_yukle('data/yorumlar.csv')

    # Okuduğum tabloyu temizliyorum.
    df = veri_temizle(df)

    # Kaç yorum kaldığını ekrana yazdırıyorum.
    # f-string → süslü parantez içindeki Python kodunu çalıştırıp
    # sonucu metnin içine yerleştiriyor.
    print(f"Toplam yorum: {len(df)}")

    # Tablonun ilk 5 satırını ekrana yazdırıyorum.
    # head() varsayılan olarak ilk 5 satırı gösterir.
    # head(10) desem ilk 10 satırı gösterirdi.
    print(df.head())