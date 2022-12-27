"""Module containing tests for Report model"""

import unittest
from models.report import Report
from models.user import User


class TestReport(unittest.TestCase):
    """Test class for Report model"""

    def test_generate(self):
        """Test for generate()"""
        user = User()
        report1 = user.reports
        Report.generate(user, **{"title": "test report"})
        report2 = user.reports
        self.assertTrue(len(report2) > len(report1))

    def test_compile(self):
        """Test for compile()"""
        pass
