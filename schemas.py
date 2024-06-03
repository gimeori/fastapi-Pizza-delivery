from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass
from fastapi import Form

@dataclass
class PizzaModel:
    pizzaname:str=Form(...)
    price:float=Form(...)
    description:str|None=Form(...)
    image:str= Form(...)
    category_name:str=Form(...)


class PizzaOrderModel(BaseModel):
    id: int
    count: int
    pizzaname: str
    image: str
    price: float
    size: str
    type: str



class OrderModel(BaseModel):
    phone: str
    name: str
    email:Optional[str|None]= None
    comment:Optional[str|None ]= None
    address:str
    pizza: List[PizzaOrderModel]
    
    
    class Config:
        orm_mode=True

class PizzaInfo(BaseModel):
    pizzaname:str
    price:float
    description:str|None
    image:str
    types:List[str]
    sizes:List[str]
    rating:Optional[int]=None
    category_name:str
    
    class Config:
        orm_mode=True
    

class OrderStatusModel(BaseModel):
    order_status:Optional[str]

    
class CategoryModel(BaseModel):
    title:str