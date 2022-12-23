"Module containing the step model"""
from models.base_model import BaseModel


class Step(BaseModel):
    """Step class"""

    info = ""
    status = ""

    def __init__(self):
        """Initialize the class"""
        super()
        self.status = "in progress"

    def update(self, **kwargs):
        """Update the cass attributes"""
        if (kwargs):
            super().update(**kwargs)

    def done(self):
        """Sets status to done"""
        self.status = "done"
