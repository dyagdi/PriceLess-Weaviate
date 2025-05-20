from datamodels import ProductObject
from client_connector import get_client
from datetime import timezone
import pandas as pd
from datetime import datetime, timezone
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_course_data_to_collection(collection_name:str, courses: list[ProductObject]):
    try:
        logger.info(f"Attempting to connect to Weaviate...")
        client = get_client()
        
        logger.info(f"Checking if collection '{collection_name}' exists...")
        collections = client.collections.list_all()
        logger.info(f"Available collections: {collections}")
        
        logger.info(f"Getting collection '{collection_name}'...")
        selected_collection = client.collections.get(collection_name)
        
        logger.info(f"Starting batch insertion of {len(courses)} objects...")
        with selected_collection.batch.dynamic() as batch:
            for i, course in enumerate(courses):
                try:
                    batch.add_object({
                        "main_category": course.main_category,
                        "name": course.name,
                        "price": course.price,
                        "high_price": course.high_price,
                        "product_link": course.product_link,
                        "image_url": course.image_url,
                        "date": course.date,
                        "market_name": course.market_name,
                    })
                    if (i + 1) % 100 == 0:
                        logger.info(f"Processed {i + 1} objects...")
                except Exception as e:
                    logger.error(f"Error adding object {i}: {str(e)}")
                    raise
        
        logger.info("Batch insertion completed successfully")
        client.close()
        
    except Exception as e:
        logger.error(f"Error in add_course_data_to_collection: {str(e)}")
        raise

from collection_creator import create_new_collection
from data_inserter import add_course_data_to_collection
from weaviate_helper import get_collection_names  

def create_if_needed_and_insert(collection_name: str, product_objects: list):
    try:
        logger.info("Getting list of existing collections...")
        collection_names = get_collection_names()
        logger.info(f"Existing collections: {collection_names}")

        if collection_name in collection_names:
            logger.info(f"Collection '{collection_name}' already exists. Adding objects...")
        else:
            logger.info(f"Collection '{collection_name}' does not exist. Creating...")
            created = create_new_collection(collection_name)
            if not created:
                raise RuntimeError(f"Failed to create collection: {collection_name}")
            logger.info("Collection created successfully")

        logger.info(f"Starting insertion of {len(product_objects)} objects...")
        add_course_data_to_collection(collection_name, product_objects)
        logger.info("Insertion complete.")
        
    except Exception as e:
        logger.error(f"Error in create_if_needed_and_insert: {str(e)}")
        raise