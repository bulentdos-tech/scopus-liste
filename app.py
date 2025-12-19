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
    
    encodings = ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']
    
    for enc in encodings:
        try:
            return pd.read_csv(file_to_load, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
        except:
            continue
    return None

df = load_data()

if df is not None:
    # Sütun isimlerini temizle
    df.columns = [c.strip() for c in df.columns]
    
    # Arama Kutusu
    query = st.text_input("Dergi Adı veya ISSN Giriniz:", "")

    if query:
        # Arama mantığı
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("Eşleşen bir dergi bulunamadı.")
    else:
        # ÖNİZLEME SİLİNDİ: Burası artık boş, kullanıcı yazana kadar bir şey görünmez.
        st.info("Sorgulama yapmak için yukarıdaki kutucuğa dergi adını veya ISSN numarasını yazın.")
else:
    st.error("HATA: CSV dosyası okunamadı.")
