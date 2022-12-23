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
        task_info = {
                "title": "Do it", 
                "description": "Just do it"
                }
        task = self.user.create_task(**task_info)
        self.assertTrue(type(task) is Task)

    def test_logged(self):
        """Test for logged()"""
        self.assertTrue(self.user.is_loggedin is False)
        self.user.logged()
        self.assertTrue(self.user.is_loggedin is True)
