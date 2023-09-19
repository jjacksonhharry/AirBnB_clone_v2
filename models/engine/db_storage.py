#!/usr/bin/python3
"""
This module defines a class to manage database storage of the airbnb_clone
"""
import os
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker


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
        url = f'mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}'
        self.__engine = create_engine(url, pool_pre_ping=True)

        if hbnb_env == "test":
            Base.metadata.drop_all(bind=self.__engine)
