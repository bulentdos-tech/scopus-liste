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
    # Tam olarak senin klasöründeki dosya ismini yazıyoruz
    file_path = "scopus dergi listesi 2025.xlsx - Sayfa1.csv"
    
    if os.path.exists(file_path):
        encodings = ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']
        for enc in encodings:
            try:
                # separator (ayraç) hatasını önlemek için sep=None kullanıyoruz
                return pd.read_csv(file_path, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
            except:
                continue
    else:
        # Eğer yukarıdaki isim tutmazsa klasördeki ilk CSV'yi bulmaya çalış
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csv_files:
            for enc in ['utf-8', 'iso-8859-9', 'cp1254', 'latin1']:
                try:
                    return pd.read_csv(csv_files[0], encoding=enc, sep=None, engine='python', on_bad_lines='skip')
                except:
                    continue
    return None

df = load_data()

# --- 4. ARAMA VE EKRAN ---
if df is not None:
    # Sütun başlıklarını temizle
    df.columns = [c.strip() for c in df.columns]
    
    query = st.text_input("Dergi Adı, ISSN veya Yayıncı Yazınız:", placeholder="Örn: Nature")

    if query:
        # Tüm satırlarda arama yap
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = df[mask]

        if not results.empty:
            st.success(f"{len(results)} sonuç bulundu.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("Eşleşen bir dergi bulunamadı.")
    else:
        st.info("Sorgulama yapmak için yukarıdaki kutuya bir kelime yazın.")
else:
    st.error("Dosya Bulunamadı! Lütfen CSV dosyasının adını kontrol edin.")
    st.write("Mevcut dosyalar:", os.listdir('.'))
