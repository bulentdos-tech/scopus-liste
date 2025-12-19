import streamlit as st
import pandas as pd
import os

# Sayfa Ayarları
st.set_page_config(page_title="Scopus 2025 Sorgulama", layout="wide")

st.title("🔍 Scopus 2025 Dergi Sorgulama")
st.markdown("---")

def load_data():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files:
        return None
    
    target = "scopus dergi listesi 2025.xlsx - Sayfa1.csv"
    file_to_load = target if target in csv_files else csv_files[0]
    
    # KARAKTER HATASINI ÇÖZEN KISIM: Farklı kodlamaları dene
    encodings = ['utf-8', 'latin1', 'iso-8859-9', 'cp1254']
    for encoding in encodings:
        try:
            return pd.read_csv(file_to_load, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return None

df = load_data()

if df is not None:
    query = st.text_input("Dergi Adı veya ISSN Giriniz:", "")

    if query:
        # Arama yaparken hata oluşmaması için boş değerleri temizle
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("Eşleşen bir dergi bulunamadı.")
    else:
        st.info("Lütfen arama yapmak için bir isim veya ISSN yazın.")
        st.write("Liste Önizlemesi:")
        st.dataframe(df.head(10))
else:
    st.error("HATA: CSV dosyası bulunamadı veya okunamadı.")
