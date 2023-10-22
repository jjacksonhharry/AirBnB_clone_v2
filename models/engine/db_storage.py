#!/usr/bin/python3
"""
This module defines a class to manage database storage of the airbnb_clone
"""
import os
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    Manages the database storage
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Create an instance
        """
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        hbnb_env = os.getenv('HBNB_ENV')
        url = (f'mysql+mysqldb://{user}:{passwd}@{host}/{db}')
        self.__engine = create_engine(url, pool_pre_ping=True)

        if hbnb_env == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Query objects from the database
        """
        objects = {}

        if cls:
            query_result = self.__session.query(cls).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            query_result = []

            for cls in classes:
                query_result.extend(self.__session.query(cls).all())

        for obj in query_result:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objects[key] = obj

        return objects

    def new(self, obj):
        """
        Add the object to the current database session
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """
        Calls the remove() method on the private session attribute
        """
        self.__session.remove()

    def reload(self):
        """
        Create all tables in the database and initialize the session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine,
            expire_on_commit=False))
        self.__session = Session()
