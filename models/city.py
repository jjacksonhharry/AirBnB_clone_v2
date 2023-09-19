#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = 'city'

    state_id = ""
    name = Column(String(128), nullable=False)

    places = relationship(
            "Place",
            back_populates="city",
            cascade="all, delete-orphan")
