"""Module containing tests for Step model"""
import unittest
from models.step import Step


class TestStep(unittest.TestCase):
    """Test class for Step model"""

    def test_done(self):
        """Test for done()"""
        step = Step()
        self.assertTrue(step.status == "in progress")
        step.done()
        self.assertTrue(step.status == "done")
