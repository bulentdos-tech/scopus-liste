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
    # Klasördeki tüm dosyaları al ve isminde '.csv' geçenleri filtrele
    all_files = os.listdir('.')
    csv_files = [f for f in all_files if f.lower().endswith('.csv')]
    
    if not csv_files:
        return None
    
    # En büyük boyutlu veya listedeki ilk CSV'yi seç (Senin dosyanı bulacaktır)
    file_to_load = csv_files[0]
    
    encodings = ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']
    for enc in encodings:
        try:
            # Virgül, noktalı virgül vb. ayraçları otomatik tespit et
            df = pd.read_csv(file_to_load, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
            return df
        except:
            continue
    return None

df = load_data()

# --- 4. ARAMA VE EKRAN ---
if df is not None:
    # Sütun başlıklarındaki boşlukları temizle
    df.columns = [str(c).strip() for c in df.columns]
    
    q = st.text_input("Dergi Adı veya ISSN Yazınız:", placeholder="Örn: Nature")

    if q:
        # Satır bazlı arama (tüm sütunlarda)
        mask = df.apply(lambda row: row.astype(str).str.contains(q, case=False, na=False).any(), axis=1)
        res = df[mask]
        
        if not res.empty:
            st.success(f"Toplam {len(res)} sonuç bulundu.")
            st.dataframe(res, use_container_width=True)
        else:
            st.warning(f"'{q}' için bir sonuç bulunamadı.")
    else:
        st.info("Sorgulama yapmak için yukarıdaki kutucuğu kullanın.")
else:
    # Hata durumunda klasörü debug için tekrar yazdıralım
    st.error("Dosya hala okunamıyor.")
    st.write("Klasördeki Dosyalar:", os.listdir('.'))
