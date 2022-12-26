"""Module containing tests for Report model"""

import unittest
from models.report import Report
from models.user import User


class TestReport(unittest.TestCase):
    """Test class for Report model"""

    def test_generate(self):
        """Test for generate()"""
        user = User()
        report = Report.generate(user, **{"title": "test report"})
        self.assertTrue(type(report) is Report)

    def test_compile(self):
        """Test for compile()"""
        pass
