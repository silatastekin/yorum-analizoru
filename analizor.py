# Transformers kütüphanesinden pipeline fonksiyonunu içe aktarıyorum.
# Pipeline, karmaşık yapay zeka modellerini tek satırda kullanmamı sağlayan bir araç.
from transformers import pipeline

# Pandas kütüphanesini içe aktarıyorum.
# Pandas, verilerimi tablo (DataFrame) formatında tutmamı ve işlememi sağlıyor.
import pandas as pd

# Kendi yazdığım veri_hazirlama.py dosyasından iki fonksiyonu çekiyorum.
# veri_yukle → CSV dosyamı okur
# veri_temizle → boş/duplike satırları temizler
from veri_hazirlama import veri_yukle, veri_temizle


# Yapay zeka modelini yükleyen fonksiyonu tanımlıyorum.
# Bu fonksiyon ilk çalıştığında modeli internetten indiriyor (~500MB),
# sonraki çalıştırmalarda ise bilgisayarımın cache'inden yüklüyor.

def model_yukle():
    # pipeline() ile Hugging Face üzerindeki hazır bir modeli kullanıyorum.
    # "text-classification" → metnin hangi sınıfa ait olduğunu bulmak istediğimi söylüyorum.
    # model= ile de Türkçe yorumlar için eğitilmiş özel bir BERT modeli seçiyorum.
    # Bu modeli ben eğitmedim; daha önce milyonlarca Türkçe metinle eğitilmiş,
    # hazır ve ücretsiz bir model — sadece kullanıyorum.
    model = pipeline(
        "text-classification",
        model="savasy/bert-base-turkish-sentiment-cased"
    )
    return model


# Tek bir yorumu analiz eden fonksiyonu tanımlıyorum.
# model → kullanacağım yapay zeka modeli
# yorum → analiz edilecek metin
def yorum_analiz_et(model, yorum):
    # BERT modeli en fazla 512 karakter işleyebilir.
    # Daha uzun yorumlar hata vermemesi için burada kırpıyorum.
    yorum = yorum[:512]
    # Modeli çalıştırıyorum ve ilk sonucu alıyorum.
    # model(yorum) bana şöyle bir şey döndürüyor:
    # [{'label': 'positive', 'score': 0.9876}]
    # [0] ile listenin ilk (ve tek) elemanını alıyorum.
    sonuc = model(yorum)[0]

    # Modelin kararını alıyorum: 'positive' ya da 'negative'
    etiket = sonuc['label']

    # Modelin ne kadar emin olduğunu gösteren skoru alıyorum.
    # 0 ile 1 arasında bir sayı — 1'e ne kadar yakınsa o kadar emin demek.
    # round() ile 3 ondalık basamağa yuvarlıyorum, daha okunabilir olsun diye.
    skor = round(sonuc['score'], 3)

    # İki değeri birlikte geri döndürüyorum.
    return etiket, skor

# Tüm tablodaki (DataFrame) yorumları tek tek analiz eden fonksiyonu tanımlıyorum.
# model → yapay zeka modeli
# df → içinde 'yorum' sütunu olan pandas tablosu
def df_analiz_et(model, df):
    # Analiz sonuçlarını geçici olarak tutacağım iki boş liste oluşturuyorum.
    etiketler = []
    skorlar = []

    # Tablodaki her yorumu tek tek dolaşıyorum.
    for yorum in df['yorum']:
        # Her yorumu az önce yazdığım fonksiyona gönderip sonucu alıyorum.
        etiket, skor = yorum_analiz_et(model, yorum)

        # Sonuçları listelerime ekliyorum.
        etiketler.append(etiket)
        skorlar.append(skor)

        # Tüm etiketleri tabloma yeni bir sütun olarak ekliyorum.
    df['etiket'] = etiketler

    # Tüm skorları tabloma yeni bir sütun olarak ekliyorum.
    df['skor'] = skorlar

    # Artık 3 sütunlu bir tablom var: yorum, etiket, skor
    return df


# Bu blok sadece bu dosyayı doğrudan çalıştırdığımda devreye giriyor.
# Başka bir dosyadan import ettiğimde bu kısım çalışmıyor.
# Yani bu blok benim "test alanım".
if __name__ == '__main__':

    # Kullanıcıya model yükleniyor bilgisini veriyorum.
    print("Model yukleniyor...")

    # Modeli yüklüyorum — ilk seferde internet bağlantısı gerekiyor.
    model = model_yukle()
    print("Model hazir!")

    # CSV dosyamı okuyorum.
    # encoding='cp1254' → Windows'un Türkçe için kullandığı karakter seti,
    # bunu belirtmezsem Türkçe karakterlerde hata alırım.
    df = veri_yukle('data/yorumlar.csv', encoding='cp1254')

    # Boş satırları, duplikeleri temizliyorum.
    df = veri_temizle(df)

    # Tüm yorumları yapay zeka ile analiz ediyorum.
    df = df_analiz_et(model, df)

    # Sadece ilgili 3 sütunu ekrana yazdırıyorum: yorum, etiket, skor
    print(df[['yorum', 'etiket', 'skor']])