from sqlalchemy import Column,Integer,ForeignKey,Table, String, ARRAY
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
import enum
Base=declarative_base()



class Pizza(Base):

    __tablename__='pizza'
    id: Mapped[int]=mapped_column(primary_key=True)
    pizzaname:Mapped[str]=mapped_column(unique=True)
    price:Mapped[float]
    description:Mapped[str | None]=mapped_column(nullable=True)
    image: Mapped[str]
    types:Mapped[str]=mapped_column(ARRAY(String))
    sizes: Mapped[str]=mapped_column(ARRAY(String))
    rating:Mapped[int]=mapped_column(nullable=True)
    category_name= Column(String, ForeignKey("category.title"))


    category=relationship('Category', back_populates='cat_pizza')
    orders = relationship('OrderPizzaTable', back_populates='pizza')
    
    def __str__(self) -> str:
        return self.pizzaname

class Category(Base):
    __tablename__='category'
    id: Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(unique=True)

    cat_pizza=relationship('Pizza', back_populates='category')

    def __str__(self) -> str:
        return self.title


class Statuses(enum.Enum):
    inprocess="inprocess"
    transit="transit"
    delivered="delivered"
    
    
class Order(Base):
    __tablename__ = 'orders'
    id : Mapped[int]=mapped_column(primary_key=True)
    phone: Mapped[str]=mapped_column(nullable=False)
    name: Mapped[str]=mapped_column(nullable=False)
    email:Mapped[str | None]=mapped_column(nullable=True)
    comment:Mapped[str | None]=mapped_column(nullable=True)
    address:Mapped[str]=mapped_column(nullable=False)

    order_status :Mapped[Statuses]

    pizzas = relationship('OrderPizzaTable', back_populates='order')

    def __str__(self) -> str:
        return self.name

class OrderPizzaTable(Base):
    __tablename__='order_pizza'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    pizza_id = Column(Integer, ForeignKey('pizza.id'), primary_key=True)
    count = Column(Integer)
    size = Column(String)
    type = Column(String)
    order = relationship(Order, back_populates='pizzas')
    pizza = relationship(Pizza, back_populates='orders')