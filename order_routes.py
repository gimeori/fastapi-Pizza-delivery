from fastapi import APIRouter,status, HTTPException
from models import Order,Pizza
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router=APIRouter(
    prefix="/orders",
    tags=['orders']
)
session=Session(bind=engine)


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel):
    pizzas = session.query(Pizza).filter(Pizza.pizzaname.in_(order.pizza)).all()
    if len(pizzas) != len(order.pizza):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Одна или несколько пицц не существуют в базе данных")

    new_order = Order(order_status='inprocess')
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    for pizza in pizzas:
        new_order.pizza.append(pizza)

    session.commit()

    order_info = [{
        "pizzaname": pizza.pizzaname
    } for pizza in new_order.pizza]

    response = {
        "order_id": new_order.id,
        "order_status": new_order.order_status,
        "order_info": order_info
    }
    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders():
      orders=session.query(Order).all()
      return jsonable_encoder(orders)

@order_router.get('/orders/{id}')
async def get_order_by_id(id:int):
     order = session.query(Order).filter(Order.id == id).first()
     if not order:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ с id {id} не найден")
     
     
     pizza_info = [{"pizzaname": pizza.pizzaname} for pizza in order.pizza]
     order_info = {
         "id": order.id,
         "name": order.name,
         "order_status": order.order_status,
         "pizza": pizza_info
     }

     return jsonable_encoder(order_info)


@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int,order:OrderStatusModel):
     order_to_update=session.query(Order).filter(Order.id==id).first()
     order_to_update.order_status=order.order_status
     session.commit()
     response={
          "id":order_to_update.id,
          "order_status":order_to_update.order_status
     }
     return jsonable_encoder(order_to_update)

@order_router.delete('/order/delete/{order_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int):
     order_to_delete=session.query(Order).filter(Order.id==id).first()
     session.delete(order_to_delete)
     session.commit()
     return order_to_delete