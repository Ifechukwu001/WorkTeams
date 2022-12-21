"""Module for the base model"""
import uuid
import datetime


class BaseModel:
    """BaseModel class"""

    def __init__(self):
        """Initializes the id of the model

        Attributes:
            id (str): UUID4 generated random id.
            created_at (datetime.DateTime): Time of creation of the instance.

        """
        self.id = uuid.uuid4()
        self.created_at = datetime.datetime.utcnow()

    def to_dict(self):
        """Returns a dictionary representation of the class

        Return:
            dict: Dicctionary representaton of the instance.

        """
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.isoformat()

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
