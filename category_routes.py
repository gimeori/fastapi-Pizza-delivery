from fastapi import APIRouter, status, HTTPException, Query
from models import Category
from schemas import CategoryModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload



category_router=APIRouter(
    prefix="/categories",
    tags=['categories']
)
session=Session(bind=engine)

@category_router.get('/')
async def list_all_items():
      items=session.query(Category).all()
      return jsonable_encoder(items)

@category_router.get('/{id}')
async def get_item_by_id(id: int, 
                         sort_by: str = Query(None, regex="^(rating|price|pizzaname)$"), 
                         order: str = Query(None, regex="^(asc|desc)$")):
    item = session.query(Category).options(selectinload(Category.cat_pizza)).filter(Category.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    pizzas = item.cat_pizza
    
    if sort_by:
        if sort_by not in ['rating', 'price', 'pizzaname']:
            raise HTTPException(status_code=400, detail="Invalid value")
        
        reverse = (order == "desc")
        
        if sort_by == "rating":
            pizzas = sorted(pizzas, key=lambda pizza: (pizza.rating is not None, pizza.rating), reverse=reverse)
        elif sort_by == "price":
            pizzas = sorted(pizzas, key=lambda pizza: pizza.price, reverse=reverse)
        elif sort_by == "pizzaname":
            pizzas = sorted(pizzas, key=lambda pizza: pizza.pizzaname, reverse=reverse)
    
    return pizzas


@category_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_item(item:CategoryModel):
    new_Category=Category(
        title=item.title,
    )
    session.add(new_Category)
    session.commit()
    return jsonable_encoder(new_Category)

@category_router.delete('/{item_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id:int):
     item_to_delete=session.query(Category).filter(Category.id==id).first()
     session.delete(item_to_delete)
     session.commit()
     return item_to_delete
