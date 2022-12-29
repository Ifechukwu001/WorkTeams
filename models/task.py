"""Module containing the task model"""
import models
from datetime import datetime
from models.base_model import BaseModel
from models.step import Step


class Task(BaseModel):
    """Task class"""

    title = ""
    description = ""
    status = ""
    deadline = None
    user_id = ""

    def __init__(self, **kwargs):
        """Initializes the instance"""
        super().__init__(**kwargs)
        self.status = "in progress"
        models.storage.new(self)

    def update(self, **kwargs):
        """Update the attributes of the Task"""
        if (kwargs):
            if "deadline" in kwargs:
                kwargs["deadline"] = datetime.fromisoformat(kwargs["deadline"])
            super().update(**kwargs)

    @property
    def steps(self):
        """Returs the steps of a task"""
        stps = []
        for stp in models.storage.all(Step):
            if stp.user_id == self.user_id and stp.task_id == self.id:
                stps.append(stp)
        return stps

    def add_deadline(self, day, month, year, hour=6, mins=0):
        """Creates the deadline"""
        date = datetime(year, month, day, hour, mins)
        self.deadline = date

    def add_step(self, step):
        """Adds a action step"""
        step.task_id = self.id

    def step_done(self, step):
        """Moves a step to finished"""
        if step in self.steps:
            step.done()

    def abandon(self):
        """Abandans the task"""
        self.status = "abandoned"
