#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, Column, \
    ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Selection(Base):
    __tablename__ = "selection"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class MenuItem(Base):
    __tablename__ = "menu_item"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(String(8))
    selection_id = Column(Integer, ForeignKey("selection.id"))
    selection = relationship(Selection)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "selection_id": self.selection_id,
        }


engine = create_engine("postgresql://catalog:catalog@localhost/catalog")
Base.metadata.create_all(engine)
