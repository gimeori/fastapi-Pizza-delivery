from fastapi import APIRouter, status, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func
from models import Pizza
from schemas import PizzaModel, PizzaInfo
from database import Session, engine
from sqlalchemy import asc, desc



pizza_router=APIRouter(
    prefix="/pizzas",
    tags=['pizzas']
)
session=Session(bind=engine)

@pizza_router.get('/')
async def list_all_items(sort_by: str = Query(None, regex="^(rating|price|pizzaname)$"), 
    order: str = Query(None, regex="^(asc|desc)$"),):
    try:
        query = session.query(Pizza)
        
        if sort_by:
            if sort_by not in ['rating', 'price', 'pizzaname']:
                raise HTTPException(status_code=400, detail="Invalid value")
            
            sort_criteria = getattr(Pizza, sort_by)
            if order == "desc":
                sort_criteria = desc(sort_criteria)
            else:
                sort_criteria = asc(sort_criteria)
            
            query = query.order_by(sort_criteria)
        
        items = query.all()
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
        item_to_update.price=item.price
        item_to_update.description=item.description
        item_to_update.pizzaname=item.pizzaname
        item_to_update.image=item.image
        item_to_update.category_name=item.category_name
        session.commit()
        return item_to_update
     except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {e}"})

@pizza_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PizzaInfo)
async def create_item(item:PizzaModel= Depends()):
    new_pizza=Pizza(
        pizzaname=item.pizzaname,
        price=item.price,
        description=item.description,
        image=item.image,
        types=["Тонкое", "Традиционное"],
        sizes=["25", "30", "35"],
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
