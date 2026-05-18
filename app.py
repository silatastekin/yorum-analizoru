# Streamlit kütüphanesini içe aktarıyorum.
# Bu kütüphane sayesinde sadece Python yazarak tarayıcıda çalışan
# bir web arayüzü oluşturabiliyorum — HTML, CSS, JavaScript bilmeme gerek yok.
import streamlit as st

# Pandas kütüphanesini içe aktarıyorum.
# CSV dosyasını okumak ve tablo işlemleri yapmak için kullanıyorum.
import pandas as pd

# Plotly kütüphanesinden express modülünü içe aktarıyorum.
# İleride pasta grafik, bar chart gibi interaktif grafikler çizmek için kullanacağım.
# Bu aşamada import ediyorum ama Aşama 5'te aktif olarak devreye girecek.
import plotly.express as px

# Kendi yazdığım analizor.py dosyasından iki fonksiyonu çekiyorum.
# model_yukle → yapay zeka modelini hazır hale getirir
# df_analiz_et → tüm yorumları analiz eder ve etiketi/skoru tabloya ekler
from analizor import model_yukle, df_analiz_et
# Kendi yazdığım veri_hazirlama.py dosyasından temizleme fonksiyonunu çekiyorum.
# veri_temizle → boş satırları, duplikeleri temizler
from veri_hazirlama import veri_temizle


# Tarayıcı sekmesinin başlığını, ikonunu ve sayfa düzenini ayarlıyorum.
# layout="wide" → sayfanın tüm genişliğini kullanıyorum, dar görünmüyor.
st.set_page_config(
    page_title="Yorum Analizoru",
    page_icon="💬",
    layout="wide"
)

# Sayfanın en üstüne büyük başlık yazıyorum.
st.title("E-Ticaret Yorum Analizoru")

# Başlığın altına açıklama metni ekliyorum.
st.markdown("CSV dosyani yukle, yorumlarini yapay zeka ile analiz et.")

# @st.cache_resource bir dekoratör — fonksiyonun sonucunu bellekte saklıyor.
# Olmadan: sayfayı her yenilemede model baştan yüklenir (~30 saniye beklerim).
# Olduğunda: model bir kez yüklenir, sonraki işlemlerde cache'den gelir.
@st.cache_resource
def get_model():
    return model_yukle()


# Kullanıcının bilgisayarından CSV dosyası yükleyebileceği bir alan oluşturuyorum.
# type=["csv"] → sadece CSV uzantılı dosyalara izin veriyorum.
# Kullanıcı dosya seçmezse yuklenen değişkeni None olur.
yuklenen = st.file_uploader(
    "CSV dosyani sec", type=["csv"]
)

# Kullanıcı bir dosya yüklediyse bu bloğa giriyorum.
if yuklenen is not None:
    # Yüklenen CSV dosyasını pandas tablosuna (DataFrame) çeviriyorum.
    # encoding='cp1254' → Türkçe karakterlerin bozulmaması için Windows encoding'i.
    df = pd.read_csv(yuklenen, encoding='cp1254')

    # Boş satırları, duplikeleri temizliyorum.
    df = veri_temizle(df)

    # Kullanıcıya kaç yorum yüklendiğini mavi bir bilgi kutusuyla gösteriyorum.
    st.info(f"Toplam {len(df)} yorum yuklendi.")

    # Mavi bir "Analiz Et" butonu oluşturuyorum.
    # type="primary" → butonun vurgulu/renkli görünmesini sağlıyor.
    # Kullanıcı butona tıkladığında aşağıdaki blok çalışıyor.
    if st.button("Analiz Et", type="primary"):

        # Analiz sürerken ekranda dönen bir yükleniyor animasyonu gösteriyorum.
        # with bloğu bitince animasyon kayboluyor.
        with st.spinner("Yorumlar analiz ediliyor..."):
            # Cache'lenmiş modeli çekiyorum — tekrar yüklenmiyor, hızlı geliyor.
            model = get_model()

            # Tüm yorumları yapay zeka ile analiz ediyorum.
            # df'e 'etiket' ve 'skor' sütunları ekleniyor.
            df = df_analiz_et(model, df)

            # Analiz sonucunu session_state'e kaydediyorum.
            # session_state → Streamlit'in sayfa yenilendiğinde veriyi
            # unutmaması için kullandığı bellek alanı.
            # Olmasaydı butona her basışta sonuçlar kaybolurdu.
            st.session_state['df'] = df

# Eğer daha önce analiz yapıldıysa ve session_state'te veri varsa bu bloğa giriyorum.
# Bu sayede kullanıcı sayfayı kaydırdığında sonuçlar kaybolmuyor.
if 'df' in st.session_state:
    df = st.session_state['df']

    # Sayfayı 3 eşit sütuna bölüyorum — yan yana metrik kartları için.
    col1, col2, col3 = st.columns(3)

    # Temel istatistikleri hesaplıyorum.
    toplam = len(df)
    olumlu = len(df[df['etiket'] == 'positive'])
    olumsuz = len(df[df['etiket'] == 'negative'])

    # Her sütuna bir metrik kartı yerleştiriyorum.
    # metric() → büyük sayı + altında küçük açıklama şeklinde gösteriyor.
    # Yüzde değerini de delta olarak gösteriyorum — yeşil/kırmızı renk alıyor.
    col1.metric("Toplam Yorum", toplam)
    col2.metric("Olumlu", olumlu, f"%{round(olumlu/toplam*100)}")
    col3.metric("Olumsuz", olumsuz, f"%{round(olumsuz/toplam*100)}")
    # Tablonun üstüne bir alt başlık ekliyorum.
    st.subheader("Yorum Sonuclari")

    # Her satıra arka plan rengi vermek için bir fonksiyon yazıyorum.
    # row → tablonun tek bir satırı
    # Etiket 'positive' ise açık yeşil, 'negative' ise açık kırmızı renk döndürüyorum.
    # len(row) kadar renk döndürüyorum çünkü her hücreye ayrı ayrı uygulanıyor.
    def renk_ver(row):
        renk = '#d4edda' if row['etiket'] == 'positive' else '#f8d7da'
        return [f'background-color: {renk}'] * len(row)
    # Tabloyu ekranda gösteriyorum.
    # style.apply(renk_ver, axis=1) → her satıra renk_ver fonksiyonumu uyguluyorum.
    # axis=1 → satır bazında işlem yap demek (0 olsaydı sütun bazında olurdu).
    # use_container_width=True → tablo sayfanın tüm genişliğini kaplasın.
    st.dataframe(
        df[['yorum', 'etiket', 'skor']].style.apply(renk_ver, axis=1),
        use_container_width=True
    )