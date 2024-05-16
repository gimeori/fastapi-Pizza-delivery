from fastapi import APIRouter, status
from models import Category
from schemas import CategoryModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder



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
async def get_item_by_id(id:int):
     item=session.query(Category).filter(Category.id==id).first()
     return jsonable_encoder(item)


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
