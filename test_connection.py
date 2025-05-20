from client_connector import get_client
from collection_creator import create_new_collection
from weaviate_helper import get_collection_names
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_weaviate_connection():
    try:
        # Test basic connection
        logger.info("Testing Weaviate connection...")
        client = get_client()
        is_ready = client.is_ready()
        logger.info(f"Connection status: {'✅ Connected' if is_ready else '❌ Not connected'}")
        
        # Test listing collections
        logger.info("\nListing existing collections...")
        collections = get_collection_names()
        logger.info(f"Found {len(collections)} collections:")
        for collection in collections:
            logger.info(f"- {collection}")
        
        # Test creating a test collection
        test_collection_name = "TestCollection"
        logger.info(f"\nTesting collection creation with name: {test_collection_name}")
        if test_collection_name in collections:
            logger.info(f"Collection {test_collection_name} already exists")
        else:
            created = create_new_collection(test_collection_name)
            logger.info(f"Collection creation {'✅ successful' if created else '❌ failed'}")
        
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    test_weaviate_connection() 