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
    #user = None

    def __init__(self):
        """Initializes the Report"""
        super()

    def update(self, **kwargs):
        """Updates the report attributes"""
        if (kwargs):
            if "time_generated" in kwargs:
                kwargs["time_generated"] = datetime.fromisoformat(kwargs["time_generated"])
            super().update(**kwargs)

    @classmethod
    def generate(cls, user, **kwargs):
        """Generate a report for a user"""
        tasks = user.tasks.copy()
        done = 0
        pending = 0
        for task in tasks:
            if task.status == "done":
                done += 1
            elif task.status == "in progress":
                pending += 1
            elif task.status == "abandoned":
                tasks.remove(task)
        kwargs["tasks"] = tasks
        kwargs["total_tasks"] = len(tasks)
        kwargs["done_tasks"] = done
        kwargs["pending_tasks"] = pending
        kwargs["time_generated"] = datetime.utcnow().isoformat()
        if "title" not in kwargs:
            kwargs["title"] = "Report for {} ({})".format(user.name, user.email)
        
        report = cls()
        report.update(**kwargs)

        return report

    @classmethod
    def compile(cls, user, subordinate=None):
        """Compile all the reports"""
        reports = []
        if user.is_admin:
            if subordinate && subordinate in user.subordinates:
                reports.append(surbordinate.reports)
            elif subordinate == None:
                for subordinate in user.subordinates:
                    reports.append(subordinate.reports)
        return reports
