from datamodels import ProductObject
from client_connector import get_client
from datetime import timezone

from datetime import datetime, timezone

from datetime import datetime, timezone

import pandas as pd
from datetime import datetime, timezone




def add_course_data_to_collection(collection_name:str, courses: list[ProductObject]):

    client = get_client()

    selected_collection = client.collections.get(collection_name)

    with selected_collection.batch.dynamic() as batch:

        for course in courses:
            batch.add_object({
        
                "main_category": course.main_category,
                "sub_category": course.sub_category,
                "lowest_category": course.lowest_category,
                "name": course.name,
                "price": course.price,
                "high_price": course.high_price,
                "in_stock": course.in_stock,
                "product_link": course.product_link,
                "page_link": course.page_link,
                "image_url": course.image_url,
                "date": course.date,
                "market_name": course.market_name,

               
                
            })
        
    
    client.close()

from collection_creator import create_new_collection
from data_inserter import add_course_data_to_collection
from weaviate_helper import get_collection_names  

def create_if_needed_and_insert(collection_name: str, product_objects: list):
    collection_names = get_collection_names()

    if collection_name in collection_names:
        print(f"ℹ️ Collection '{collection_name}' already exists. Adding objects...")
    else:
        print(f"🆕 Collection '{collection_name}' does not exist. Creating...")
        created = create_new_collection(collection_name)
        if not created:
            raise RuntimeError(f"Failed to create collection: {collection_name}")

    print(f"📦 Inserting {len(product_objects)} objects...")
    add_course_data_to_collection(collection_name, product_objects)
    print("✅ Insertion complete.")