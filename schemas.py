from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass
from fastapi import UploadFile, File, Form

class OrderModel(BaseModel):
    id:Optional[int]
    order_status:str="inprocess"
    pizza:List[str]
    
    
    class Config:
        orm_mode=True


@dataclass
class PizzaModel:
    pizzaname:str=Form(...)
    price:float=Form(...)
    description:str=Form(...)
    image:UploadFile= File(...)
    sizes:List[str]=Form(...)
    category_name:str=Form(...)


class PizzaInfo(BaseModel):
    pizzaname:str
    price:float
    description:str
    image:str
    sizes:List[str]
    rating:Optional[int]=None
    category_name:str
    
    class Config:
        orm_mode=True
    

class OrderStatusModel(BaseModel):
    order_status:Optional[str]

    
class CategoryModel(BaseModel):
    id: Optional[int]
    title:str