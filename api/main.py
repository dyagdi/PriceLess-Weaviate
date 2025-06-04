from http.client import HTTPException
from fastapi import FastAPI, Query
from typing import List, Optional
from weaviate_helper import semantic_search_for_relevant_data_objects , query_all_by_name, get_data_objects_for_given_collection
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ProductResponse(BaseModel):
    main_category: Optional[str]
    name: Optional[str]
    price: Optional[float]
    high_price: Optional[float]
    market_name: Optional[str]
    product_link: Optional[str]
    image_url: Optional[str]

@app.get("/search", response_model=List[ProductResponse])
def search_products(
    query: str = Query(..., description="Aranacak kelime"),
    collection: str = Query("SupermarketProducts3"),
    limit: int = Query(20, ge=1, le=20)
):
    try:
        results = semantic_search_for_relevant_data_objects(
            collection_name=collection,
            user_query=query,
            reference_count=limit
        )

        response_data = []

        for res in results:
            props = res.properties

            response_data.append({
                "main_category": props.get("main_category"),
                "name": props.get("name"),
                "price": props.get("price"),
                "high_price": props.get("high_price"),
                "market_name": props.get("market_name"),
                "product_link": props.get("product_link"),
                "image_url": props.get("image_url")
            })

        return response_data

    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return []


class PriceHistoryItem(BaseModel):
    name: str
    price: float
    date: str
    market_name: Optional[str]

from datetime import date, datetime

@app.get("/price-history", response_model=List[PriceHistoryItem])
def price_history(
    name: str = Query(..., description="Product name to fetch price history for"),
):
    results = query_all_by_name("SupermarketProducts2", name)
    results += query_all_by_name("SupermarketProducts3", name)

    history = []
    for obj in results:
        props = obj.properties if hasattr(obj, 'properties') else obj
        raw_date = props.get("date")
        # Convert date/datetime objects to ISO string
        if isinstance(raw_date, (date, datetime)):
            date_str = raw_date.isoformat()
        else:
            date_str = str(raw_date) if raw_date is not None else None

        history.append({
            "name": props.get("name"),
            "price": props.get("price"),
            "date": date_str,
            "market_name": props.get("market_name"),
        })

    history.sort(key=lambda x: x["date"] or "")
    return history

@app.get("/chatbot/products", response_model=List[ProductResponse])
def get_products_for_chatbot(
    collection: str = Query("SupermarketProducts3", description="Collection name to fetch products from"),
    offset: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of products to return")
):
    """
    Endpoint for chatbot service to get all products from a given collection
    with pagination support for better performance
    """
    try:
        # Get all objects from the collection
        all_objects = get_data_objects_for_given_collection(collection)
        
        # Apply pagination
        total_count = len(all_objects)
        paginated_objects = all_objects[offset:offset + limit]
        
        response_data = []
        for obj in paginated_objects:
            response_data.append({
                "main_category": obj.get("main_category"),
                "name": obj.get("name"),
                "price": obj.get("price"),
                "high_price": obj.get("high_price"),
                "market_name": obj.get("market_name"),
                "product_link": obj.get("product_link"),
                "image_url": obj.get("image_url")
            })

        print(f"[INFO] Chatbot endpoint: Retrieved {len(response_data)} products (offset: {offset}, limit: {limit}, total: {total_count})")
        return response_data

    except Exception as e:
        print(f"[ERROR] Chatbot products endpoint failed: {e}")
        return []

@app.get("/chatbot/collections")
def get_available_collections():
    """
    Endpoint for chatbot to get list of available collections
    """
    try:
        from weaviate_helper import get_collection_names
        collections = get_collection_names()
        return {"collections": collections}
    except Exception as e:
        print(f"[ERROR] Get collections failed: {e}")
        return {"collections": []}