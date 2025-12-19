import streamlit as st
import pandas as pd
import os

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Scopus 2025 Sorgulama", layout="wide")

st.title("🔍 Scopus 2025 Dergi Sorgulama")
st.markdown("---")

# CSV Dosyasını Bulma ve Yükleme
def load_data():
    # Klasördeki tüm CSV dosyalarını listele
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files:
        return None
    
    # Varsa senin özel dosyanı, yoksa bulduğu ilk CSV'yi yükle
    target = "scopus dergi listesi 2025.xlsx - Sayfa1.csv"
    file_to_load = target if target in csv_files else csv_files[0]
    
    return pd.read_csv(file_to_load)

df = load_data()

if df is not None:
    # Arama Kutusu
    query = st.text_input("Dergi Adı veya ISSN Giriniz:", "")

    if query:
        # Arama mantığı: Herhangi bir sütunda bu metin geçiyor mu?
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("Eşleşen bir dergi bulunamadı.")
    else:
        st.info("Lütfen arama yapmak için bir isim veya ISSN yazın.")
        st.write("Liste Önizlemesi (İlk 10 Satır):")
        st.dataframe(df.head(10))
else:
    st.error("HATA: CSV dosyası bulunamadı. Lütfen GitHub'a dosyanızı yüklediğinizden emin olun.")
