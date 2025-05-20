import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force reload of environment variables
load_dotenv(override=True)

wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
#cohere_key = os.getenv("COHERE_API_KEY")
#gemini_api_key = os.getenv("GEMINI_API_KEY")



def cloud_client():
    try:
        # Print all environment variables for debugging
        logger.info("Current environment variables:")
        logger.info(f"WCD_URL: {wcd_url}")
        logger.info(f"WCD_API_KEY: {wcd_api_key[:5]}...{wcd_api_key[-5:] if wcd_api_key else 'None'}")
        logger.info(f"OPENAI_API_KEY: {openai_api_key[:5]}...{openai_api_key[-5:] if openai_api_key else 'None'}")
        
        logger.info(f"Attempting to connect to Weaviate Cloud at: {wcd_url}")
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=wcd_url,
            auth_credentials=Auth.api_key(wcd_api_key),
            headers={
                "X-OpenAI-Api-Key": openai_api_key,
            },
            skip_init_checks=False,
        )
        
        # Test the connection
        is_ready = client.is_ready()
        logger.info(f"Connection test result: {'Success' if is_ready else 'Failed'}")
        
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Weaviate Cloud: {str(e)}")
        raise

# def local_client():
#     client = weaviate.connect_to_local(
#         port=8080,  
#         grpc_port=50051,
#         headers={
#             "X-OpenAI-Api-Key": openai_api_key,
#             "X-Cohere-Api-Key": cohere_key
#         }
#     )
#     return client

def get_client():
    try:
        client = cloud_client()
        return client
    except Exception as e:
        logger.error(f"Error in get_client: {str(e)}")
        raise