import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv


load_dotenv()

wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
#cohere_key = os.getenv("COHERE_API_KEY")
#gemini_api_key = os.getenv("GEMINI_API_KEY")



def cloud_client():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=wcd_url,
        auth_credentials=Auth.api_key(wcd_api_key),
        headers={
            "X-OpenAI-Api-Key": openai_api_key,

            },
        skip_init_checks=True,
    )
    return client

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
    # return local_client()
    return cloud_client()