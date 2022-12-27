"Module containing the step model"""
import models
from models.base_model import BaseModel


class Step(BaseModel):
    """Step class"""

    info = ""
    status = ""
    task_id = ""
    user_id = ""

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        self.status = "in progress"
        models.storage.new(self)

    def update(self, **kwargs):
        """Update the cass attributes"""
        if (kwargs):
            super().update(**kwargs)

    def done(self):
        """Sets status to done"""
        self.status = "done"
