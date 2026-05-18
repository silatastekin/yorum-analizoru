# yorum-analizoru

Türkçe müşteri yorumlarını yapay zeka ile otomatik olarak **olumlu** veya **olumsuz** olarak sınıflandıran, Streamlit ile çalışan interaktif bir dashboard uygulaması.

---

#Özellikler

- CSV dosyası yükleyerek toplu yorum analizi yapabilirsiniz
- Hugging Face üzerindeki Türkçe BERT modeli ile yüksek doğruluklu sınıflandırma
- Her yorum için olumlu/olumsuz etiketi ve güven skoru (0-1 arası)
- Olumlu yorumlar yeşil, olumsuz yorumlar kırmızı renkle gösterilir
- Toplam yorum, olumlu ve olumsuz sayılarını gösteren özet metrikler
- Tamamen ücretsiz ve açık kaynak

---

#Kullanılan Teknolojiler

| Teknoloji | Amaç |
|-----------|------|
| Python | Temel programlama dili |
| Streamlit | Web arayüzü |
| Hugging Face Transformers | Yapay zeka modeli |
| BERT (savasy/bert-base-turkish-sentiment-cased) | Türkçe duygu analizi |
| Pandas | Veri okuma ve temizleme |
| Plotly | İnteraktif grafikler |


---

## Proje Yapısı

---

## ⚙️ Kurulum

### 1. Repoyu klonla
```bash
git clone https://github.com/silatastekin/yorum-analizoru.git
cd yorum-analizoru
```

### 2. Sanal ortam oluştur ve aktive et
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Kütüphaneleri yükle
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı başlat
```bash
streamlit run app.py
```

Tarayıcı otomatik olarak `http://localhost:8501` adresinde açılır.

---

##  Kullanım

1. Uygulamayı başlattıktan sonra tarayıcıda dashboard açılır
2. **"CSV dosyanı seç"** alanından yorum içeren CSV dosyanı yükle
3. **"Analiz Et"** butonuna tıkla
4. Yapay zeka her yorumu analiz eder ve sonuçları gösterir
5. Yeşil satırlar olumlu, kırmızı satırlar olumsuz yorumları temsil eder

### CSV Formatı

CSV dosyanın şu formatta olması gerekir:
Tek sütun yeterli — sütun adı `yorum` olmalı.

---

## Model Hakkında

Bu projede [savasy/bert-base-turkish-sentiment-cased](https://huggingface.co/savasy/bert-base-turkish-sentiment-cased) modeli kullanılmaktadır. Model, Türkçe metinler üzerinde eğitilmiş bir BERT modelidir ve duygu analizi (sentiment analysis) görevinde yüksek başarı göstermektedir.

İlk çalıştırmada model otomatik olarak indirilir (~500MB). Sonraki çalıştırmalarda cache'den yüklenir.

---

## Geliştirici

**Sıla Taştekin**  
[github.com/silatastekin](https://github.com/silatastekin)

---

## Lisans

Bu proje açık kaynaklıdır ve serbestçe kullanılabilir.
