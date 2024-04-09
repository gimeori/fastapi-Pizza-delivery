
from sqlalchemy import Column,Integer,ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base=declarative_base()

order_pizza_association = Table(
    'order_pizza',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('pizza_id', Integer, ForeignKey('pizza.id'))
)

class Pizza(Base):

    __tablename__='pizza'
    id: Mapped[int]=mapped_column(primary_key=True)
    pizzaname:Mapped[str]=mapped_column(unique=True)
    price:Mapped[float]
    description:Mapped[str]

    orders = relationship('Order', secondary=order_pizza_association, back_populates='pizza')
    



class Statuses(enum.Enum):
    inprocess="inprocess"
    transit="transit"
    delivered="delivered"
    
    
class Order(Base):
    __tablename__ = 'orders'
    id : Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[datetime]=mapped_column(default=func.now())
    order_status :Mapped[Statuses]

    pizza = relationship('Pizza', secondary=order_pizza_association, back_populates='orders')





