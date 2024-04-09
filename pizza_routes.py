from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from models import Pizza
from schemas import PizzaModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder


pizza_router=APIRouter(
    prefix="/pizzas",
    tags=['pizzas']
)
session=Session(bind=engine)

@pizza_router.get('/items')
async def list_all_items():
      items=session.query(Pizza).all()
      return jsonable_encoder(items)

@pizza_router.get('/items/{id}')
async def get_item_by_id(id:int):
     item=session.query(Pizza).filter(Pizza.id==id).first()
     return jsonable_encoder(item)

@pizza_router.put('/item/update/{item_id}/')
async def update_item(id:int,item:PizzaModel):
     item_to_update=session.query(Pizza).filter(Pizza.id==id).first()
     item_to_update.price=item.price
     item_to_update.description=item.description
     session.commit()
     response={
          "id":item_to_update.id,
          "price":item_to_update.price,"description": item_to_update.description,
          "pizzaname":item_to_update.pizzaname
     }
     return jsonable_encoder(item_to_update)

@pizza_router.post('/item', status_code=status.HTTP_201_CREATED)
async def create_item(item:PizzaModel):
    new_pizza=Pizza(
        pizzaname=item.pizzaname,
        price=item.price,
        description=item.description
    )
    
    session.add(new_pizza)
    session.commit()
    response={
        "pizzaname":new_pizza.pizzaname,
        "price": new_pizza.price,
        "id":new_pizza.id,
        "description":new_pizza.description
    }
    return jsonable_encoder(response)

@pizza_router.delete('/item/delete/{item_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id:int):
     item_to_delete=session.query(Pizza).filter(Pizza.id==id).first()
     session.delete(item_to_delete)
     session.commit()
     return item_to_delete
