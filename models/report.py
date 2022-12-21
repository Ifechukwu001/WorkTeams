"""Module containing the report model"""
from models.base_model import BaseModel
from datetime import datetime


class Report(BaseModel):
    """Report class"""
    time_generated = None
    title = ""
    summary = ""
    tasks = []
    total_tasks = 0
    done_tasks = 0
    pending_tasks = 0

    def __init__(self):
        """Initializes the Report"""
        super()

    def update(self, **kwargs):
        """Updates the report attributes"""
        if (kwargs):
            if "time_generated" in kwargs:
                kwargs["time_generated"] = datetime.fromisoformat(kwargs["time_generated"])
            super.update(**kwargs)
