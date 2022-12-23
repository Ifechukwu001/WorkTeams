"""Module containing the task model"""
from models.base_model import BaseModel
from datetime import datetime


class Task(BaseModel):
    """Task class"""

    title = ""
    description = ""
    status = ""
    steps = []
    deadline = None

    def __init__(self):
        """Initializes the instance"""
        super()
        self.status = "in progress"

    def update(self, **kwargs):
        """Update the attributes of the Task"""
        if (kwargs):
            if "deadline" in kwargs:
                kwargs["deadline"] = datetime.fromisoformat(kwargs["deadline"])
            super().update(**kwargs)

    def add_deadline(self, day, month, year, hour=6, mins=0):
        """Creates the deadline"""
        date = datetime(year, month, day, hour, mins)
        self.deadline = date

    def add_step(self, step):
        """Adds a action step"""
        self.steps.append(step)

    def step_done(self, step):
        """Moves a step to finished"""
        if step in self.steps:
            step.done()

    def abandon(self):
        """Abandans the task"""
        self.status = "abandoned"
