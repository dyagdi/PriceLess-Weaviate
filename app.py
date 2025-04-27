import streamlit as st

st.set_page_config(
    page_title="Süpermarket Ürün Eşleştirme",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.header(":shopping_cart: Süpermarket Ürün Karşılaştırma Paneli", divider="rainbow")

col_left, col_middle, col_right = st.columns([1, 0.05, 1])

# ---- Sol Panel: Tanıtım ----
greetings_container = col_left.container(border=True)
greetings_container.subheader(":rocket: Hadi Başlayalım!", divider="gray")
greetings_container.markdown("**Market ürünlerini veri tabanına yükleyin ve semantik olarak karşılaştırın.**")

greetings_container.markdown("""
:bookmark_tabs: Soldaki menüyü kullanarak şu işlemleri yapabilirsiniz:
* :package: Ürünleri veritabanından alıp Weaviate'a yükleyin
* :mag: Semantik arama yaparak benzer ürünleri keşfedin
""")

process_info_container = col_right.container(border=True)
process_info_container.subheader(":gear: Uygulama Akışı", divider="gray")
process_info_container.markdown("""
1. :file_folder: Veritabanından ürünleri filtreleyerek alın  
2. :inbox_tray: Ürünleri Weaviate koleksiyonuna yükleyin  
3. :mag_right: Weaviate üzerinden semantik arama yapın
""")

col_1, col_2, col_3 = st.columns([0.2, 0.6, 0.2])
with col_2:
    st.markdown("### ➡️ İşlem Seçin")

    if st.button(":package: Ürünleri DB'den Al & Weaviate'a Aktar", use_container_width=True, type="primary"):
        st.switch_page("pages/1-Ürün Yükleme.py")

    if st.button(":mag: Semantik Arama Yap", use_container_width=True):
        st.switch_page("pages/2-Arama Motoru.py")
