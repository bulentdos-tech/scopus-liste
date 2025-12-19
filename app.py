import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS ---
GA_ID = "G-ZYJGZJXNPF" 
ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
    </script>
"""
components.html(ga_code, height=0)

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Scopus 2025 Sorgulama", page_icon="📚", layout="wide")
st.title("🔍 Scopus 2025 Dergi Sorgulama")
st.markdown("---")

# --- 3. VERİ YÜKLEME ---
@st.cache_data
def load_data():
    files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    if not files:
        return None
    
    # Klasördeki ilk CSV dosyasını al
    f_path = files[0]
    for enc in ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']:
        try:
            return pd.read_csv(f_path, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
        except:
            continue
    return None

df = load_data()

# --- 4. ARAMA VE EKRAN ---
if df is not None:
    df.columns = [c.strip() for c in df.columns]
    q = st.text_input("Dergi Adı veya ISSN Yazınız:", placeholder="Örn: Nature")

    if q:
        mask = df.apply(lambda row: row.astype(str).str.contains(q, case=False, na=False).any(), axis=1)
        res = df[mask]
        if not res.empty:
            st.success(f"Toplam {len(res)} sonuç bulundu.")
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("Sonuç bulunamadı.")
    else:
        st.info("Sorgulama yapmak için yukarıdaki kutucuğu kullanın.")
else:
    st.error("HATA: CSV dosyası bulunamadı.")
