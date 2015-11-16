from db_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DbSession = sessionmaker(bind=engine)
session = DbSession()

myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheesePizza = MenuItem(name="Cheese Pizza", description="Made with natural ingredients", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesePizza)
session.commit()

print(session.query(Restaurant).all())
