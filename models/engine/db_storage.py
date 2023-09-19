#!/usr/bin/python3
"""
This module defines a class to manage database storage of the airbnb_clone
"""
import os
from os import getenv
from sqlalchemy import create_engine, MetaData
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
        mysql_user = os.getenv('HBNB_MYSQL_USER')
        mysql_pwd = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        mysql_db = os.getenv('HBNB_MYSQL_db')
        hbnb_env = os.getenv('HBNB_ENV')
        url = (
            f'mysql+mysqldb://{mysql_user}:{mysql_pwd}@'
            f'{mysql_host}/{mysql_db}'
            )
        self.__engine = create_engine(url, pool_pre_ping=True)

        if hbnb_env == "test":
            Base.metadata.drop_all(bind=self.__engine)

        Base.metadata.create_all(self.__engine)

        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

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
                key = "{}.{}".format(type(obj).__name__, obj.id)
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
            if obj:
                self.__session.commit()

        def delete(self, obj=None):
            """
            Delete from the current database session
            """
            if obj:
                self.__session.delete(obj)

        def reload(self):
            """
            Create all tables in the database and initialize the session
            """
            Base.metadata.create_all(self.__engine)
            self.__session = scoped_session(sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))
