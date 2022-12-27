"""Module containing tests for user model"""
import unittest
from models.user import User
from models.task import Task
from models.report import Report


class TestUser(unittest.TestCase):
    """Test class for User"""

    def setUp(self):
        self.user = User()
        info = {
                "name": "John Doe",
                "email": "example@mail.com",
                "password": "password",
                }
        self.user.update(**info)

    def test_create_task(self):
        """Test for create_task()"""
        tasks = self.user.tasks
        task_info = {
                "title": "Do it", 
                "description": "Just do it"
                }
        self.user.create_task(**task_info)
        self.assertTrue(len(self.user.tasks) - len(tasks) == 1)

    def test_logged(self):
        """Test for logged()"""
        self.assertTrue(self.user.is_loggedin is False)
        self.user.logged()
        self.assertTrue(self.user.is_loggedin is True)

    def test_create_report(self):
        """Test for create_report()"""
        reports = self.user.reports
        self.user.create_report(title="Work test")
        self.assertTrue(len(self.user.reports) - len(reports) == 1)

    def test_create_admin(self):
        """Test for create_admin()"""
        sub = User()
        sub.update(admin_id=self.user.id)
        self.user.is_admin = True
        self.assertFalse(sub.is_admin)
        self.user.create_admin(sub)
        self.assertTrue(sub.is_admin)

    def test_create_subordinate(self):
        """Test for create_subordinate"""
        subs = self.user.subordinates
        self.user.is_admin = True
        self.user.create_subordinate("Jack Cole", "example_test@mail.com")
        self.assertTrue((len(self.user.subordinates) - len(subs)) == 1)
