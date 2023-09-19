#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # for dbstorage
    cities = relationship('City', backref='state', cascade='all, delete-orphan')

    # for file storage
    @property
    def cities(self):
        city_objects = storage.all('City')
        city_list = []
        for city in city_objects.values():
            if city.state_id = self.id:
                city_list.append(city)
        return city_list
