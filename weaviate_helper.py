from weaviate.classes.query import MetadataQuery, Filter, Rerank
import requests
import json
from client_connector import get_client
from collection_creator import adjust_first_letter_of_collection_name


def get_data_objects_for_given_collection(collection_name):
    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()
    collection = client.collections.get(collection_name)
    
    data_objects = []
    for obj in collection.iterator():
        data_object = {
            "main_category": obj.properties.get("main_category", ""),
            "name": obj.properties.get("name", ""),
            "price": obj.properties.get("price", ""),
            "high_price": obj.properties.get("high_price", ""),
            "product_link": obj.properties.get("product_link", ""),
            "image_url": obj.properties.get("image_url", ""),
            "date": obj.properties.get("date", ""),
            "market_name": obj.properties.get("market_name", ""),
           

        }
        data_objects.append(data_object)
           
    client.close()
    return data_objects

def get_collection_names():
    existing_collections = get_list_of_collections()

    collection_names = [collection for collection in existing_collections]

    return collection_names


def get_collection(collection_name):
    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()
 
    collection = client.collections.get(collection_name)
 
    client.close()
 
    return collection

def get_list_of_collections():

    client = get_client()

    existing_collections = client.collections.list_all()

    client.close()

    return existing_collections


def delete_collection(collection_name):
    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()

    client.collections.delete(collection_name)
    client.close()

    existing_collections = get_list_of_collections()
    deletion_status = True if collection_name not in [collection for collection in existing_collections] else False

    return deletion_status


def add_data_to_collection(collection_name, data):
    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()

    selected_collection = client.collections.get(collection_name)

    with selected_collection.batch.dynamic() as batch:  
        for d in data:
            batch.add_object({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })
            
def fetch_test_data():
    resp = requests.get(
        "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
    )
    data = json.loads(resp.text)
    return data

def semantic_search_for_relevant_data_objects(collection_name, user_query, reference_count):
    if not user_query:
        raise ValueError("Query must not be None")

    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()
    selected_collection = client.collections.get(collection_name)

    response = selected_collection.query.near_text(
        query=user_query,
        limit=reference_count,
        return_metadata=MetadataQuery(certainty=True)
    )

    client.close()
    return response.objects
    

def query_all_by_name(collection_name, product_name):
    collection_name = adjust_first_letter_of_collection_name(collection_name)
    client = get_client()
    collection = client.collections.get(collection_name)
    
    matched_objects = []
    for obj in collection.iterator():
        obj_name = obj.properties.get("name", "")
        if obj_name == product_name:  
            matched_objects.append(obj)
    client.close()
    return matched_objects    