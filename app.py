import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Scopus 2025 Rehberi", page_icon="📚", layout="centered")

# Başlık ve Açıklama
st.title("🔍 Scopus 2025 Dergi Sorgulama")
st.markdown("Güncel Scopus listesinde dergi durumunu (Aktif/Pasif) hızlıca sorgulayın.")

# Veriyi yükleme fonksiyonu
@st.cache_data
def load_data():
    # Temizlediğin dosyanın tam adını buraya yaz
    df = pd.read_csv("scopus dergi listesi 2025.xlsx - Sayfa1.csv")
    return df

try:
    data = load_data()

    # Arama kutusu
    query = st.text_input("Dergi Adı veya ISSN giriniz...", placeholder="Örn: Nature veya 1234-5678")

    if query:
        # Arama filtresi (Büyük/küçük harf duyarsız)
        results = data[
            data['Source Title'].str.contains(query, case=False, na=False) | 
            data['ISSN'].astype(str).str.contains(query, na=False)
        ]

        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            # Sonuçları göster
            for index, row in results.iterrows():
                with st.expander(f"📖 {row['Source Title']}"):
                    st.write(f"**Durum:** {row['Active or Inactive']}")
                    st.write(f"**ISSN:** {row['ISSN']}")
                    st.write(f"**Yayıncı:** {row['Publisher']}")
                    st.write(f"**Kapsam:** {row['Coverage']}")
        else:
            st.error("Eşleşen bir dergi bulunamadı. Lütfen yazımı kontrol edin.")
    else:
        st.info("Arama yapmak için yukarıya bir isim yazın.")

except Exception as e:
    st.error("Dosya yüklenirken bir hata oluştu. Lütfen CSV dosya adının doğruluğundan emin olun.")