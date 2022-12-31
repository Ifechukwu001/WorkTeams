"Module containing the step model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Step(BaseModel, Base):
    """Step class"""
    if models.storage_t == "db":
        __tablename__ = "step"
        info = Column(String(128), nullable=False)
        status = Column(String(20), nullable=False)
        task_id = Column(ForeignKey("task.id"), nullable=False)
        user_id = Column(ForeignKey("user.id"), nullable=False)

    info = ""
    status = ""
    task_id = ""
    user_id = ""

    def __init__(self, **kwargs):
        """Initialize the class"""
        super().__init__(**kwargs)
        self.status = "in progress"
        models.storage.new(self)

    def update(self, **kwargs):
        """Update the cass attributes"""
        if (kwargs):
            super().update(**kwargs)

    def done(self):
        """Sets status to done"""
        self.status = "done"
