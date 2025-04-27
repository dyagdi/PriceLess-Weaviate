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

selected_table = st.selectbox("🛍️ Hangi marketten ürünleri yüklemek istiyorsun?", market_tables)

collection_name = st.text_input("🗂️ Weaviate Koleksiyon İsmi", value="SupermarketProducts")

if st.button("📥 Veritabanından Ürünleri Yükle ve Göster"):

    with st.spinner(f"{selected_table} tablosundan ürünler alınıyor..."):
        conn = get_pg_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT id, main_category, sub_category, lowest_category, name, price, high_price, 
                   in_stock, product_link, page_link, image_url, date, market_name
            FROM {selected_table}
        """) 

        rows = cursor.fetchall()
        conn.close()

        if rows:
            st.success(f"{len(rows)} ürün yüklendi ({selected_table}).")

            df = pd.DataFrame(rows, columns=[
                "id", "main_category", "sub_category", "lowest_category", "name", "price", "high_price",
                "in_stock", "product_link", "page_link", "image_url", "date", "market_name"
            ])
            st.dataframe(df.head(20), use_container_width=True)

            product_objects = [
                ProductObject(
                    id=row[0],
                    main_category=row[1],
                    sub_category=row[2],
                    lowest_category=row[3],
                    name=row[4],
                    price=row[5],
                    high_price=row[6],
                    in_stock=row[7],
                    product_link=row[8],
                    page_link=row[9],
                    image_url=row[10],
                    date=row[11],
                    market_name=row[12]
                ) for row in rows
            ]

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