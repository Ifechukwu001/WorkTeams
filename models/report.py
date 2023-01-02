"""Module containing the report model"""
import os
import models
from datetime import datetime
from models.base_model import BaseModel, Base
from models.task import Task
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship



class Report(BaseModel, Base):
    """Report class"""
    if models.storage_t == "db":
        __tablename__ = "report"
        time_generated = Column(DateTime)
        title = Column(String(128), nullable=False)
        summary = Column(String(256))
        total_tasks = Column(Integer)
        done_tasks = Column(Integer)
        pending_tasks = Column(Integer)
        user_id = Column(String(50), ForeignKey("user.id"))
        user = relationship("User", back_populates="reports")

    else:
        time_generated = None
        title = ""
        summary = ""
        total_tasks = 0
        done_tasks = 0
        pending_tasks = 0
        user_id = ""

    def __init__(self, **kwargs):
        """Initializes the Report"""
        super().__init__(**kwargs)
        models.storage.new(self)

    def update(self, **kwargs):
        """Updates the report attributes"""
        if (kwargs):
            if "time_generated" in kwargs:
                kwargs["time_generated"] = datetime.fromisoformat(kwargs["time_generated"])
            super().update(**kwargs)

    @property
    def tasks(self):
        """Return the tasks of the report"""
        tsks = []
        for tsk in models.storage.all(Task):
            if tsk.user_id == self.user_id and self.time_generated > tsk.created_at:
                if tsk.status != "abandoned":
                    tsks.append(tsk)
        return tsks

    @classmethod
    def generate(cls, user, **kwargs):
        """Generate a report for a user"""
        tasks = user.tasks
        done = 0
        pending = 0
        for task in tasks:
            if task.status == "done":
                done += 1
            elif task.status == "in progress":
                pending += 1
            elif task.status == "abandoned":
                tasks.remove(task)
        kwargs["total_tasks"] = len(tasks)
        kwargs["done_tasks"] = done
        kwargs["pending_tasks"] = pending
        date = datetime.utcnow()
        kwargs["time_generated"] = date.isoformat()
        kwargs["user_id"] = user.id
        if "title" not in kwargs:
            kwargs["title"] = "Report for {} ({}) on {}".format(user.name, user.email, date.date())
        
        report = cls()
        report.update(**kwargs)

        models.storage.save()

    @classmethod
    def compile(cls, user, subordinate=None):
        """Compile all the reports"""
        reports = []
        if user.is_admin:
            if subordinate and subordinate in user.subordinates:
                reports.append(surbordinate.reports)
            elif subordinate == None:
                for subordinate in user.subordinates:
                    reports.append(subordinate.reports)
        return reports
