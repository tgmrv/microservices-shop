from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: str

class ProductReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    category: str