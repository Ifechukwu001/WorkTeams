"""Module containing the user model"""
from datetime import datetime
import models
from models.base_model import BaseModel
from models.report import Report
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
    admin_id = ""
    #subordinates = []
    #tasks = []
    #reports = []

    def __init__(self):
        """Initialize the instance"""
        super().__init__()

    def update(self, **kwargs):
        """Update the attribute of the User"""
        if (kwargs):
            if "last_login" in kwargs:
                kwargs["last_login"] = datetime.fromisoformat(kwargs["last_login"])
            super().update(**kwargs)

    @property
    def subordinates(self):
        """Return subordinates"""
        subs = []
        if self.is_admin:
            for sub in models.storage.all(self.__class__):
                if sub.admin_id == self.id:
                    subs.append(sub)
        return subs

    @property
    def tasks(self):
        """Return the tasks of a user"""
        tsks = []
        for tsk in models.storage.all(Task):
            if tsk.user_id == self.id:
                tsks.append(tsk)
        return tsks

    @property
    def reports(self):
        """Returns the reports of a user"""
        rpts = []
        for rpt in models.storage.all(Report):
            if rpt.user_id == self.id:
                rpts.append(rpt)
        return rpts
        
    def create_task(self, **kwargs):
        """Creates a new task instance"""
        task = Task()
        if "id" in kwargs:
            kwargs.pop("id")
        if "created_at" in kwargs:
            kwargs.pop("created_at")
        kwargs["user_id"] = self.id
        task.update(**kwargs)

        models.storage.save()

    def create_report(self, **kwargs):
        """Creates a new report instance"""
        if "id" in kwargs:
            kwargs.pop("id")
        if "created_at" in kwargs:
            kwargs.pop("created_at")
        Report.generate(self, **kwargs)

        models.storage.save()

    def logged(self):
        """Manages the logged status of a user"""
        if self.is_loggedin == False:
            self.last_login = datetime.utcnow()
            self.is_loggedin = True
        else:
            self.is_loggedin = False

    def create_admin(self, user):
        """Creates a new admin"""
        if self.is_admin and user in self.subordinates:
            user.is_admin = True

    def create_subordinate(self, name, email, admin_id=None):
        """Create a new subordinate"""
        admin = self.id
        if admin_id != None:
            admin = admin_id
        if self.is_admin:
            sub = self.__class__()
            sub.update(name=name, email=email, password=email, admin_id=admin)

            models.storage.save()
