import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType, Configure, VectorDistances
from datamodels import ProductObject
from client_connector import get_client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def adjust_first_letter_of_collection_name(collection_name):
    adjusted_name = collection_name[0].upper() + collection_name[1:]
    logger.info(f"Adjusted collection name from '{collection_name}' to '{adjusted_name}'")
    return adjusted_name

from weaviate.classes.config import DataType, Property

def build_properties_from_product_objects():
    try:
        logger.info("Building properties from ProductObject model...")
        datamodel_properties = ProductObject.get_property_names(ProductObject)
        schema_properties = []

        for prop in datamodel_properties:
            if prop in ["price", "high_price"]:
                schema_properties.append(Property(name=prop, data_type=DataType.NUMBER))
            elif prop == "date":
                schema_properties.append(Property(name=prop, data_type=DataType.DATE))
            else:
                schema_properties.append(Property(name=prop, data_type=DataType.TEXT))
        
        logger.info(f"Created schema properties: {[p.name for p in schema_properties]}")
        return schema_properties
    except Exception as e:
        logger.error(f"Error building properties: {str(e)}")
        raise

def create_new_collection(collection_name):
    try:
        logger.info(f"Creating new collection: {collection_name}")
        client = get_client()
        
        # Check if collection already exists
        existing_collections = client.collections.list_all()
        if collection_name in existing_collections:
            logger.warning(f"Collection '{collection_name}' already exists")
            return True
        
        schema_properties = build_properties_from_product_objects()
        
        logger.info("Creating collection with schema...")
        new_collection = client.collections.create(
            name=collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_openai(model="text-embedding-3-large"),
            generative_config=Configure.Generative.openai(),
            properties=schema_properties,
            vector_index_config=Configure.VectorIndex.hnsw(
                distance_metric=VectorDistances.COSINE,
            )
        )

        collection_name = adjust_first_letter_of_collection_name(collection_name)
        status = True if new_collection.name == collection_name else False
        
        if status:
            logger.info(f"Successfully created collection: {collection_name}")
        else:
            logger.error(f"Failed to create collection: {collection_name}")
        
        client.close()
        return status
        
    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        raise

