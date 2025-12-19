import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Scopus 2025 Sorgulama", layout="wide")

# DOSYA ADINI BURADAN AYARLIYORUZ
# GitHub'a yüklediğin dosya adı neyse buraya onu yaz:
DOSYA_ADI = "scopus dergi listesi 2025.xlsx - Sayfa1.csv"

@st.cache_data
def load_data():
    if os.path.exists(DOSYA_ADI):
        return pd.read_csv(DOSYA_ADI)
    else:
        st.error(f"Sistem dosyayı bulamadı! Aranan isim: {DOSYA_ADI}")
        st.info("GitHub'daki dosya adınız ile koddaki ismin aynı olduğundan emin olun.")
        return None

st.title("🔍 Scopus 2025 Dergi Listesi")

df = load_data()

if df is not None:
    search = st.text_input("Dergi adı veya ISSN girin:", "")
    if search:
        # Arama sonuçlarını filtrele
        results = df[
            df.iloc[:, 0].str.contains(search, case=False, na=False) | # 1. sütunda ara (Genelde Source Title)
            df.iloc[:, 1].astype(str).str.contains(search, na=False)   # 2. sütunda ara (Genelde ISSN)
        ]
        
        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            st.dataframe(results)
        else:
            st.warning("Sonuç bulunamadı.")
