from pydantic import BaseModel
from typing import Optional, List
import enum

class OrderModel(BaseModel):
    id:Optional[int]
    order_status:str="inprocess"
    pizza:List[str]


class PizzaModel(BaseModel):
    id:Optional[int]
    pizzaname:str
    price:Optional[int]
    description:str
    

class OrderStatusModel(BaseModel):
    order_status:Optional[str]

    