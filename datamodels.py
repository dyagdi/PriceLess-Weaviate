from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Type, Optional


class ProductObject(BaseModel):
    id: int = Field(..., description="The unique identifier of the product")
    main_category: str = Field(..., description="The main category of the product")
    sub_category: str = Field(..., description="The sub-category of the product")
    lowest_category: Optional[str] = Field(..., description="The lowest category of the product")
    name: str = Field(..., description="The name of the product")
    price: Optional[float] = Field(..., description="The price of the product")
    high_price: Optional[float] = Field(None, description="The high price of the product")
    in_stock: bool = Field(..., description="Whether the product is in stock")
    product_link: str = Field(..., description="The link to the product page")
    page_link: str = Field(..., description="The link to the product category page")
    image_url: Optional[str] = Field(..., description="The URL of the product image")
    date: datetime = Field(..., description="The date when the product was added")
    market_name: str = Field(..., description="The name of the market where the product is sold")
    @staticmethod
    def get_property_names(cls: Type[BaseModel]) -> List[str]:
        """Returns a list of all property names for the given Pydantic model class"""
        return list(cls.model_fields.keys())
