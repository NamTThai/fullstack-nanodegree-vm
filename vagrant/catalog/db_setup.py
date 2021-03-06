from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import create_engine
import json
import string

Base = declarative_base()


class Type(Base):
    """Pokemon Type

    Args:
        id:  category id
        name:  name of that category
    """

    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    pokemons = relationship('Pokemon')


class User(Base):
    """Store email address of Pokemon Entry's creator

    Args:
        id: user id
        email: user email
    """

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=False)


class Pokemon(Base):
    """Pokemon information

    Args:
        id:  item id, PRIMARY KEY
        name: item name
        category_id:  corresponding category
        description:  item description
        user_id:  id of entry creator, can be null if the entry is
            automatically generated
        date_entered:  when the item was entered, default to insertion time

    """

    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    description = Column(String(250))
    img_url = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    date_entered = Column(DateTime, default=func.now())
    type = relationship(Type)
    user = relationship(User)

    def getIconUrl(self):
        """If the image url is from serebii.net, there will be a corresponding
        icon url"""
        if string.find(self.img_url, "serebii") > -1:
            self.icon_url = string.replace(self.img_url, "xy/pokemon",
                                           "pokedex-xy/icon")
        else:
            self.icon_url = self.img_url
        return self.icon_url

    def getJSON(self):
        """Get JSON representation of this object"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.name,
            "description": self.description,
            "img_url": self.img_url,
            "user_email": self.getUserEmail()
        }

    def getUserEmail(self):
        """Get email of creator user. None is automatically generated"""
        if self.user is None:
            return None
        else:
            return self.user.email


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)

if __name__ == '__main__':
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Add default types
    TYPES = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice",
             "Fighting", "Poison", "Rock", "Flying", "Psychic", "Bug",
             "Ground", "Ghost", "Dark", "Dragon", "Steel", "Fairy"]
    for type in TYPES:
        newType = Type(name=type)
        session.add(newType)
        session.commit()

    # Add default pokemons
    with open('data/starter_pkm.json') as starter_data:
        starters = json.load(starter_data)
    for starter in starters:
        type_id = session.query(Type).filter_by(name=starter["type"]).one().id
        newEntry = Pokemon(name=starter["name"], type_id=type_id,
                           description=starter["description"],
                           img_url=starter["img_url"])
        session.add(newEntry)
        session.commit()
