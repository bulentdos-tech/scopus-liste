import streamlit as st
import pandas as pd
import os

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Scopus 2025 Rehberi", layout="wide")

st.title("🔍 Scopus 2025 Dergi Sorgulama Sistemi")
st.markdown("---")

# --- DOSYA YÜKLEME BÖLÜMÜ ---
@st.cache_data
def load_data():
    # Klasördeki tüm dosyaları tara ve .csv olanı bul
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    # Öncelikle senin belirttiğin ismi ara
    target_name = "scopus dergi listesi 2025.xlsx - Sayfa1.csv"
    
    if target_name in files:
        return pd.read_csv(target_name)
    elif len(files) > 0:
        # Eğer o isimde yoksa, klasördeki ilk bulduğu CSV'yi yükle (Hata önleyici)
        return pd.read_csv(files[0])
    else:
        return None

try:
    df = load_data()

    if df is not None:
        # Arama Kutusu
        search_query = st.text_input("Dergi Adı, ISSN veya Yayıncı Giriniz:", placeholder="Örn: Nature veya 1234-5678")

        if search_query:
            # Arama filtresi: Tüm sütunlarda ara
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            results = df[mask]

            if not results.empty:
                st.success(f"{len(results)} adet sonuç bulundu.")
                
                # Tabloyu göster
                st.dataframe(results, use_container_width=True)
                
                # İstatistiksel özet (Opsiyonel)
                if 'Active or Inactive' in results.columns:
                    st.sidebar.subheader("Durum Özeti")
                    st.sidebar.write(results['Active or Inactive'].value_counts())
            else:
                st.warning("Eşleşen bir kayıt bulunamadı. Lütfen farklı bir anahtar kelime deneyin.")
        else:
            st.info("Sorgulama yapmak için yukarıdaki alana yazmaya başlayın.")
            st.write("Şu an sistemde toplam", len(df), "kayıtlı dergi/kaynak bulunuyor.")
            st.dataframe(df.head(10)) # İlk 10 satırı önizleme olarak
