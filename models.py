from sqlalchemy import Column,Integer,ForeignKey,Table, String, ARRAY
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
import enum
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
    description:Mapped[str | None]=mapped_column(nullable=True)
    image: Mapped[str]
    types:Mapped[str]=mapped_column(ARRAY(String))
    sizes: Mapped[str]=mapped_column(ARRAY(String))
    rating:Mapped[int]=mapped_column(nullable=True)
    category_name= Column(String, ForeignKey("category.title"))


    orders = relationship('Order', secondary=order_pizza_association, back_populates='pizza')
    category=relationship('Category', back_populates='cat_pizza')
    
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

    pizza = relationship('Pizza', secondary=order_pizza_association, back_populates='orders')

    def __str__(self) -> str:
        return self.name

