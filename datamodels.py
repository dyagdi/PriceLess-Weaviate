from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Type, Optional


class ProductObject(BaseModel):
    main_category: str = Field(..., description="The main category of the product")
    name: str = Field(..., description="The name of the product")
    price: Optional[float] = Field(..., description="The price of the product")
    high_price: Optional[float] = Field(None, description="The high price of the product")
    product_link: str = Field(..., description="The link to the product page")
    image_url: Optional[str] = Field(..., description="The URL of the product image")
    date: datetime = Field(..., description="The date when the product was added")
    market_name: Optional[str] = Field(None, description="The name of the market where the product is sold")
    @staticmethod
    def get_property_names(cls: Type[BaseModel]) -> List[str]:
        """Returns a list of all property names for the given Pydantic model class"""
        return list(cls.model_fields.keys())
