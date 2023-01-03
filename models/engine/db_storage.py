"""Module containing the file storage model"""
import json
from os import getenv
from models.base_model import Base
from models.user import User
from models.task import Task
from models.report import Report
from models.step import Step
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"User": User, "Task": Task, "Report": Report, "Step": Step}


class DBStorage:
    """DataBase storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the storage"""
        WT_USER = getenv("WT_USER")
        WT_PASS = getenv("WT_PASS")
        WT_HOST = getenv("WT_HOST")
        WT_DB = getenv("WT_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(WT_USER,
            WT_PASS,
            WT_HOST,
            WT_DB))
        

    def all(self, cls=None):
        """Returns a list of all objects of a class or all classes"""
        objs = []
        if cls:
            objs = self.__session.query(cls).all()
        else:
            for clss in classes:
                obj = self.__session.query(classes[clss]).all()
                objs.extend(obj)
        return objs

    def new(self, obj):
        """Add a new object to the storage"""
        self.__session.add(obj)

    def save(self):
        """Saves the current state of the application"""
        self.__session.commit()

    def load(self):
        """Loads the objects from the storage to the application"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session
