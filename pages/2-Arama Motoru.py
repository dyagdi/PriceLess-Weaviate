# pages/1-SemanticSearch.py

import streamlit as st
from weaviate.classes.query import MetadataQuery

from weaviate_helper import semantic_search_for_relevant_data_objects
from client_connector import get_client

st.set_page_config(page_title="🔍 Ürün Arama", layout="wide")
st.title("🔍 Semantik Ürün Arama")

collection_name = st.text_input("🔢 Koleksiyon Adı", value="SupermarketProducts")
user_query = st.text_input("💬 Ne aramak istiyorsun?", placeholder="örnek: sek süt 1lt")
reference_count = st.slider("🔢 Kaç sonuç gösterilsin?", 1, 20, 5)

if st.button("🔍 Ara"):
    if not user_query:
        st.warning("Lütfen bir arama sorgusu girin.")
    else:
        with st.spinner("Semantik arama yapılıyor..."):
            try:
                results = semantic_search_for_relevant_data_objects(
                    collection_name=collection_name,
                    user_query=user_query,
                    reference_count=reference_count
                )

                if not results:
                    st.info("Sonuç bulunamadı.")
                else:
                    st.success(f"{len(results)} sonuç bulundu:")

                    for res in results:
                        props = res.properties

                        name = props.get("name", "İsimsiz Ürün")
                        market = props.get("market_name", "Bilinmiyor")
                        main_category = props.get("main_category", "")
                        sub_category = props.get("sub_category", "")
                        lowest_category = props.get("lowest_category", "")
                        price = props.get("price", "Belirsiz")
                        link = props.get("product_link", "#")
                        image_url = props.get("image_url")

                        st.markdown(f"""
                            **🛍️ {name}**
                            - Market: `{market}`
                            - Kategori: {main_category} > {sub_category} > {lowest_category}
                            - Fiyat: **{price} TL**
                            - Link: [Ürün Sayfası]({link})
                        """)

                        if image_url:
                            st.image(image_url, width=150)

                        st.markdown("---")
            except Exception as e:
                st.error(f"❌ Arama sırasında hata oluştu: {e}")