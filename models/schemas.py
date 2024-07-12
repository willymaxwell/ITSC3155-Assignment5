from pydantic import BaseModel
from typing import Optional

class SandwichBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class SandwichCreate(SandwichBase):
    pass

class SandwichUpdate(SandwichBase):
    pass

class SandwichRead(SandwichBase):
    id: int

    class Config:
        orm_mode = True

class ResourceBase(BaseModel):
    name: str
    quantity: int

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    pass

class ResourceRead(ResourceBase):
    id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    sandwich_id: int
    resource_id: int
    quantity: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: str
    date: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True

class OrderDetailBase(BaseModel):
    order_id: int
    sandwich_id: int
    quantity: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(OrderDetailBase):
    pass

class OrderDetailRead(OrderDetailBase):
    id: int

    class Config:
        orm_mode = True
