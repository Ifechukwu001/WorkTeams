"""Module containing the user model"""
import os
from datetime import datetime
import models
from models.base_model import BaseModel
from models.report import Report
from models.task import Task
from models.step import Step


class User(BaseModel):
    """User Class"""

    name = ""
    email = ""
    password = ""
    workspace = ""
    last_login = None
    is_loggedin = False
    is_admin = False
    admin_id = ""

    def __init__(self, **kwargs):
        """Initialize the instance"""
        super().__init__(**kwargs)

    def update(self, **kwargs):
        """Update the attribute of the User"""
        if (kwargs):
            if "last_login" in kwargs:
                kwargs["last_login"] = datetime.fromisoformat(kwargs["last_login"])
            if "workspace" in kwargs:
                os.makedirs(kwargs["workspace"], exist_ok=True)
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
        if "deadline" in kwargs:
            deadline = kwargs.pop("deadline")
            deadline = [int(i) for i in deadline]
        if "steps" in kwargs:
            steps = kwargs.pop("steps")
            for step in steps:
                st = Step()
                st.update(info=step, task_id=task.id, user_id=self.id)
        kwargs["user_id"] = self.id
        task.update(**kwargs)
        task.add_deadline(*deadline)

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
        workspace = "{}/{}".format(models.home, name.split()[0])
        if admin_id != None:
            admin = admin_id
        if self.is_admin:
            sub = self.__class__()
            sub.update(name=name, email=email, password=email, admin_id=admin, workspace=workspace)

            models.storage.save()
