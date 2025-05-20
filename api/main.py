from fastapi import FastAPI, Query
from typing import List, Optional
from weaviate_helper import semantic_search_for_relevant_data_objects , query_all_by_name
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

@app.get("/price-history", response_model=List[PriceHistoryItem])
def price_history(
    name: str = Query(..., description="Product name to fetch price history for"),
):
    results = query_all_by_name("SupermarketProducts", name)
    results += query_all_by_name("SupermarketProducts2", name)
    results += query_all_by_name("SupermarketProducts3", name)

    history = []
    for obj in results:
        props = obj.properties if hasattr(obj, 'properties') else obj
        history.append({
            "name": props.get("name"),
            "price": props.get("price"),
            "date": props.get("date"),
            "market_name": props.get("market_name"),
        })

    history.sort(key=lambda x: x["date"])

    return history