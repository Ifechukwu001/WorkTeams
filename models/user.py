"""Module containing the user model"""
import os
from datetime import datetime
import models
from models.base_model import BaseModel, Base
from models.report import Report
from models.task import Task
from models.step import Step
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


class User(BaseModel, Base):
    """User Class"""
    if models.storage_t == "db":
        __tablename__ = "user"
        name = Column(String(30))
        email = Column(String(30), unique=True, nullable=False)
        password = Column(String(30), nullable=False)
        workspace = Column(String(128), unique=True)
        last_login = Column(DateTime, default=None)
        is_loggedin = Column(Boolean, default=False)
        is_admin = Column(Boolean, default=False)
        admin_id = Column(String(50), ForeignKey("user.id"))

    else:
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
        steps = []
        if "steps" in kwargs:
            steps = kwargs.pop("steps")
        kwargs["user_id"] = self.id
        deadline = []
        if "deadline" in kwargs:
            dline = kwargs.pop("deadline")
            deadline = [int(i) for i in dline if i]
        task.update(**kwargs)
        if steps:
            for step in steps:
                st = Step()
                st.update(info=step, user_id=self.id)
                task.add_step(st)
        if deadline:
            task.add_deadline(*deadline)

        models.storage.save()
        return task.id

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
        workspace = "{}/{}".format(models.home, email.split("@")[0])
        if admin_id != None:
            admin = admin_id
        if self.is_admin:
            sub = self.__class__()
            sub.update(name=name, email=email, password=email, admin_id=admin, workspace=workspace)

            models.storage.save()

    def add_subtask(self, **kwargs):
        """Create a task for subordinate"""
        if "subordinate" in kwargs and self.is_admin:
            subordinate = kwargs.pop("subordinate")
            for sub in self.subordinates:
                if sub.email == subordinate:
                    sub.create_task(**kwargs)
                    return
        
    def check_subreport(self, sub_mail, year, month, day):
        if self.is_admin:
            for sub in self.subordinates:
                if sub.email == sub_mail:
                    limit_date = datetime(year, month, day)
                    reports = [report for report in sub.reports if report.time_generated > limit_date]
                    return reports
                    