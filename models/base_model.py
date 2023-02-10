"""Module for the base model"""
import os
import uuid
import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

if os.getenv("WT_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel class"""
    if os.getenv("WT_STORAGE") == "db":
        id = Column(String(50), default=str(uuid.uuid4()), unique=True, primary_key=True)
        created_at = Column(DateTime, default=str(datetime.datetime.utcnow()))

    def __init__(self, **kwargs):
        """Initializes the id of the model

        Attributes:
            id (str): UUID4 generated random id.
            created_at (datetime.DateTime): Time of creation of the instance.

        """
        if kwargs:
            kwargs.pop("__class__")
            self.update(**kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.utcnow()
            models.storage.new(self)

    def to_dict(self):
        """Returns a dictionary representation of the class

        Return:
            dict: Dicctionary representaton of the instance.

        """
        new_dict = self.__dict__.copy()
        for key, value in new_dict.items():
            if type(value) is datetime.datetime:
                new_dict[key] = value.isoformat()
        if "_sa_instance_state" in new_dict:
            new_dict.pop("_sa_instance_state")
        if "__class__" not in new_dict:
            new_dict["__class__"] = self.__class__.__name__

        return new_dict

    def update(self, **kwargs):
        """Updates the attributes of the class

        Args:
            kwargs (:obj:`dict`): Dictionary of attributes to be updated.

        """
        if (kwargs):
            for attribute, value in kwargs.items():
                if (attribute == "created_at"):
                    value = datetime.datetime.fromisoformat(value)
                self.__setattr__(attribute, value)
            models.storage.save()

    def __repr__(self):
        """Representation of the class"""
        return str(self.to_dict())
