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
