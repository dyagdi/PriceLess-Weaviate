import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_env_loading():
    # Get the absolute path of the .env file
    env_path = os.path.abspath('.env')
    logger.info(f"Looking for .env file at: {env_path}")
    
    # Check if file exists
    if os.path.exists(env_path):
        logger.info("✅ .env file found")
    else:
        logger.error("❌ .env file not found")
        return
    
    # Load environment variables
    load_dotenv(env_path)
    
    # Get and log the values
    wcd_url = os.getenv("WCD_URL")
    wcd_api_key = os.getenv("WCD_API_KEY")
    
    logger.info(f"WCD_URL: {wcd_url}")
    logger.info(f"WCD_API_KEY: {wcd_api_key[:5]}...{wcd_api_key[-5:] if wcd_api_key else 'None'}")

if __name__ == "__main__":
    test_env_loading() 