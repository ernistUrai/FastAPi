from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    price: float
    description: str
    
    class Config:
        from_attibutes = True        