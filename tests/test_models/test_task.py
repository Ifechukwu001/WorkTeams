"""Module for testing the task class"""
import unittest
from datetime import datetime
from models.task import Task
from models.step import Step


class TestTask(unittest.TestCase):
    """Test class for Task model"""

    def setUp(self):
        self.task = Task()
        info = {
                "title": "Do it",
                "description": "Just do it",
                }
        self.task.update(**info)

        self.step = Step()
        self.step.update(**{"info": "First code..."})
 

    def test_add_deadline(self):
        """Test for add_deadline()"""
        year = 2023
        month = 1
        day = 31
        hour = 14
        mins = 0
        date = datetime(year, month, day, hour, mins)
        self.task.add_deadline(day, month, year, hour, mins)
        self.assertTrue(self.task.deadline, date)

    def test_add_step(self):
        """Test for add_step()"""
        self.task.add_step(self.step)
        self.assertTrue(self.step in self.task.steps)

    def test_step_done(self):
        """Test for step_done"""
        self.assertTrue(self.step.status == "in progress")
        self.task.add_step(self.step)
        self.task.step_done(self.step)
        self.assertTrue(self.step.status == "done")

    def test_abandon(self):
        """Test for abandon()"""
        self.assertTrue(self.task.status != "abandoned")
        self.task.abandon()
        self.assertTrue(self.task.status == "abandoned")
