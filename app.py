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

# --- 3. AKILLI VERİ YÜKLEME ---
@st.cache_data
def load_data():
    # Klasördeki tüm dosyaları tara ve sonu .csv ile biten İLK dosyayı al
    csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    
    if not csv_files:
        return None
    
    # Bulduğu ilk CSV dosyasını seçer (İsim ne olursa olsun)
    file_to_load = csv_files[0]
    
    encodings = ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']
    for enc in encodings:
        try:
            # Ayraçları (virgül/noktalı virgül) otomatik tanır, hatalı satırları atlar
            return pd.read_csv(file_to_load, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
        except:
            continue
    return None

df = load_data()

# --- 4. ARAMA VE EKRAN ---
if df is not None:
    # Sütun başlıklarını temizle
    df.columns = [c.strip() for c in df.columns]
    
    query = st.text_input("Dergi Adı, ISSN veya Yayıncı Yazınız:", placeholder="Örn: Nature veya 2034-9130")

    if query:
        # Arama mantığı: Herhangi bir sütunda bu metin geçiyor mu?
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(
