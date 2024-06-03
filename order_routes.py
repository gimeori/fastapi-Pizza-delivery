from fastapi import APIRouter,status, HTTPException
from models import Order,Pizza
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from sqlalchemy.sql import func

order_router=APIRouter(
    prefix="/orders",
    tags=['orders']
)
session=Session(bind=engine)


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel):
    pizza_ids = [pizza.id for pizza in order.pizza]
    pizzas = session.query(Pizza).filter(Pizza.id.in_(pizza_ids)).all()

    if len(pizzas) != len(order.pizza):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Одна или несколько пицц не существуют в базе данных")

    new_order = Order(
         phone=order.phone,
         name=order.name,
         email=order.email,
         comment=order.comment,
         address=order.address,
         order_status='inprocess'
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    for pizza_order in order.pizza:
        pizza = next((p for p in pizzas if p.id == pizza_order.id), None)
        if pizza:
            for _ in range(pizza_order.count):
                new_order.pizza.append(pizza)

    session.commit()

    for pizza in pizzas:
        rating_count = session.query(func.count(Order.id)).filter(Order.pizza.contains(pizza)).scalar()
        pizza.rating = rating_count

    session.commit()

    order_info = [{
        "pizzaname": pizza_order.pizzaname,
        "count": pizza_order.count
    } for pizza_order in order.pizza]

    response = {
        "order_id": new_order.id,
        "order_status": new_order.order_status,
        "order_info": order_info
    }
    return response

@order_router.get('/orders')
async def list_all_orders():
      orders=session.query(Order).all()
      return orders

@order_router.get('/orders/{id}')
async def get_order_by_id(id:int):
     order = session.query(Order).filter(Order.id == id).first()
     if not order:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ с id {id} не найден")
     
     
     pizza_info = [{"pizzaname": pizza.pizzaname} for pizza in order.pizza]
     order_info = {
         "id": order.id,
         "phone":order.phone,
         "name": order.name,
         "order_status": order.order_status,
         "pizza": pizza_info
     }
     return order_info



@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int,order:OrderStatusModel):
     order_to_update=session.query(Order).filter(Order.id==id).first()
     order_to_update.order_status=order.order_status
     session.commit()
     response={
          "id":order_to_update.id,
          "order_status":order_to_update.order_status
     }
     return order_to_update

@order_router.delete('/order/delete/{order_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int):
     order_to_delete=session.query(Order).filter(Order.id==id).first()
     session.delete(order_to_delete)
     session.commit()
     return order_to_delete