#CONFIGURATION CODE
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base=declarative_base()

##CLASS SETUP CODE

class Restaurant(Base):
    __tablename__="Restaurant"

class Menu_Item(Base):
    __tablename__="menu_item"

#CONFIGURATION CODE
engine=create_engine("sqlite:///restaurantmenu.db")

Base.metadata.createall(engine)