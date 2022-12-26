"""Module containing the user model"""
from datetime import datetime
from models.base_model import BaseModel
from models.task import Task


class User(BaseModel):
    """User Class"""

    name = ""
    email = ""
    password = ""
    workspace = ""
    daily_hours = 0
    total_hours = 0
    last_login = None
    is_loggedin = False
    is_admin = False
    subordinates = []
    tasks = []
    reports = []

    def __init__(self):
        """Initialize the instance"""
        super()

    def update(self, **kwargs):
        """Update the attribute of the User"""
        if (kwargs):
            if "last_login" in kwargs:
                kwargs["last_login"] = datetime.fromisoformat(kwargs["last_login"])
            super().update(**kwargs)
        
    def create_task(self, **kwargs):
        """Creates a new task instance"""
        task = Task()
        if "id" in kwargs:
            kwargs.pop("id")
        if "created_at" in kwargs:
            kwargs.pop("created_at")
        task.update(**kwargs)
        self.tasks.append(task)

        return task

    def create_report(self, **kwargs):
        """Creates a new report instance"""
        if "id" in kwargs:
            kwargs.pop("id")
        if "created_at" in kwargs:
            kwargs.pop("created_at")
        report = Report.generate(self, **kwargs)
        self.reports.append(report)

    def logged(self):
        """Manages the logged status of a user"""
        if self.is_loggedin == False:
            self.last_login = datetime.utcnow()
            self.is_loggedin = True
        else:
            self.is_loggedin = False

    def create_admin(self, user):
        """Creates a new admin"""
        if self.is_admin && user in self.subordinates:
            user.is_admin = True

    def create_subordinate(self, name, email):
        """Create a new subordinate"""
        sub = self()
        sub.update(name=name, email=email, password=email)
        self.subordintes.append(sub)
        return sub

