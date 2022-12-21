"""Module containing the task model"""
from models.base_model import BaseModel
from datetime import datetime


class Task(BaseModel):
    """Task class"""

    title = ""
    description = ""
    status = ""
    steps = []
    steps_done = []
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
            super.update(**kwargs)

    def add_deadline(self, day, month, year, hour=6, mins=0):
        """Creates the deadline"""
        date = datetime(year, month, day, hour, mins)
        self.deadline = date

    def add_step(self, step):
        """Adds a action step"""
        self.steps.append(step)

    def done_step(self, step):
        """Moves a step to finished"""
        if step in self.steps:
            self.steps_done.append(step)

        step_sorted = steps.copy()
        step.sorted.sort()
        done_sorted = steps_done.copy()
        done_sorted.sort()
        if step_sorted == done_sorted:
            self.status = "done"

    def abandon(self):
        """Abandans the task"""
        self.status = "abandoned"
