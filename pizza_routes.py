from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from models import Pizza, Order
from schemas import PizzaModel, PizzaInfo
from database import Session, engine
import os
from utils.save_image import image_add_origin


pizza_router=APIRouter(
    prefix="/pizzas",
    tags=['pizzas']
)
session=Session(bind=engine)

@pizza_router.get('/')
async def list_all_items():
    try:
      items=session.query(Pizza).all()
      return items
    except Exception as e:
                return JSONResponse(status_code=500, content={"message": f"Error: {e}"})

@pizza_router.get('/{id}')
async def get_item_by_id(id:int):
     try:
        item=session.query(Pizza).filter(Pizza.id==id).first()
        if not item:
            return JSONResponse(status_code=404, content={"message": "Item not found"})
        return item
     except Exception as e:
          return JSONResponse(status_code=500, content={"message": f"Error: {e}"})

@pizza_router.put('/update/{item_id}/', response_model=PizzaInfo)
async def update_item(id:int,item:PizzaModel=Depends()):
     try:
        item_to_update=session.query(Pizza).filter(Pizza.id==id).first()
        path_folder='static/images/products'
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)
        path_image=image_add_origin(item.image,path_folder)
        item_to_update.price=item.price
        item_to_update.description=item.description
        item_to_update.pizzaname=item.pizzaname
        item_to_update.image=path_image
        item_to_update.pastry=item.pastry
        item_to_update.sizes=item.sizes
        item_to_update.category_name=item.category_name
        session.commit()
        return item_to_update
     except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {e}"})

@pizza_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PizzaInfo)
async def create_item(item:PizzaModel= Depends()):
    path_folder='static/images/products'
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
    path_image=image_add_origin(item.image,path_folder)
    new_pizza=Pizza(
        pizzaname=item.pizzaname,
        price=item.price,
        description=item.description,
        image=path_image,
        pastry=item.pastry,
        sizes=item.sizes,
        category_name=item.category_name,
    )
    session.add(new_pizza)
    session.commit()
    return new_pizza

@pizza_router.delete('/{item_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id:int):
     try:
        item_to_delete=session.query(Pizza).filter(Pizza.id==id).first()
        session.delete(item_to_delete)
        session.commit()
        return item_to_delete
     except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {e}"})


@pizza_router.patch('/{id}/')
async def update_rating_status(id: int):
    pizza_to_update = session.query(Pizza).filter(Pizza.id == id).first()
    if not pizza_to_update:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

    rating_count = session.query(func.count(Order.id)).filter(Order.pizza.contains(pizza_to_update)).scalar()
    pizza_to_update.rating = rating_count
    session.commit()

    return pizza_to_update