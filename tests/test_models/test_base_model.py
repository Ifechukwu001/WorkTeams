"""Module containing tests for the module base_model"""
from models.base_model import BaseModel
import unittest


class TestBaseModel(unittest.TestCase):
    """Test class for BaseModel"""

    def test_to_dict(self):
        base1 = BaseModel()

        base1_dict = base1.to_dict()
        self.assertEqual(base1.id, base1_dict["id"])
        self.assertEqual(base1.created_at.isoformat(), base1_dict["created_at"])

    def test_update(self):
        base2 = BaseModel()

        info = {"id": "new_id", "created_at": "2022-12-21T11:47:58.099834"}
        base2.update(**info)
        self.assertEqual(info["id"], base2.id)
        self.assertEqual(info["created_at"], base2.created_at.isoformat())
