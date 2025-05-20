import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

from datamodels import ProductObject
import collection_creator
import data_inserter
import pandas as pd
from data_inserter import create_if_needed_and_insert
load_dotenv()

def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD")
    )

st.set_page_config(page_title="Market Product Uploader", layout="wide")
st.title("🛒 Süpermarket Ürün Aktarıcı")

market_tables = [
    "migros_products",
    "sokmarket_products",
    "carrefour_products",
    "marketpaketi_products",
    "mopas_products",
  
]

"""
    "migros_3_products",
    "sokmarket_3_products",
    "carrefour_3_products",
    "marketpaketi_3_products",
    "mopas_3_products",
    "a101_3_products",
]
"""
selected_table = st.selectbox("🛍️ Hangi marketten ürünleri yüklemek istiyorsun?", market_tables)

collection_name = st.text_input("🗂️ Weaviate Koleksiyon İsmi", value="SupermarketProducts2")

if st.button("📥 Veritabanından Ürünleri Yükle ve Göster"):
    with st.spinner(f"{selected_table} tablosundan ürünler alınıyor..."):
        conn = get_pg_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT main_category, name, price, high_price, 
                   product_link, image_url, date, market_name
            FROM {selected_table}
        """) 

        rows = cursor.fetchall()
        conn.close()

        if rows:
            st.success(f"{len(rows)} ürün yüklendi ({selected_table}).")

            df = pd.DataFrame(rows, columns=[
                "main_category", "name", "price", "high_price",
                "product_link", "image_url", "date", "market_name"
            ])
            st.dataframe(df.head(20), use_container_width=True)

            product_objects = []
            for row in rows:
                try:
                    product = ProductObject(
                        main_category=row[0],
                        name=row[1],
                        price=row[2],
                        high_price=row[3],
                        product_link=row[4],
                        image_url=row[5],
                        date=row[6],
                        market_name=row[7] if row[7] is not None else None
                    )
                    product_objects.append(product)
                except Exception as e:
                    st.error(f"Error creating product object: {str(e)}")
                    continue

            st.session_state.product_objects = product_objects
        else:
            st.warning("Hiç ürün bulunamadı.")

if st.button("📦 Ürünleri Yükle"):
    if "product_objects" not in st.session_state:
        st.error("Lütfen önce ürünleri yükleyin.")
    else:
        try:
            create_if_needed_and_insert(collection_name, st.session_state.product_objects)
            st.success("🎉 Ürünler başarıyla yüklendi!")
        except Exception as e:
            st.error(f"❌ Hata: {e}")