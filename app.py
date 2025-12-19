import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS AYARI ---
# Senin verdiğin özel kod buraya eklendi
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
# Google Analytics'i sayfaya gizlice gömüyoruz
components.html(ga_code, height=0)

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Scopus 2025 Sorgulama", page_icon="📚", layout="wide")

st.title("🔍 Scopus 2025 Dergi Sorgulama")
st.info("Kasım 2025 güncel Scopus verileriyle arama yapın.")
st.markdown("---")

# --- 3. VERİ YÜKLEME (HATA ÖNLEYİCİ) ---
@st.cache_data
def load_data():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files:
        return None
    
    # Senin temizlediğin dosya adı
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

# --- 4. ARAMA VE SONUÇLAR ---
if df is not None:
    # Sütun isimlerini (boşluklar dahil) temizle
    df.columns = [c.strip() for c in df.columns]
    
    query = st.text_input("Dergi Adı, ISSN veya Yayıncı Yazınız:", placeholder="Örn: Nature veya 2034-9130")

    if query:
        # Tüm sütunlarda arama yap (küçük/büyük harf duyarsız)
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(f"Toplam {len(results)} sonuç bulundu.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning(f"'{query}' araması için bir sonuç bulunamadı.")
    else:
        st.write("Sorgulama yapmak için yukarıdaki kutucuğu kullanın.")
else:
    st.error("Sistem CSV dosyasını bulamadı. Lütfen GitHub deponuzu kontrol edin.")
