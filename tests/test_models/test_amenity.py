#!/usr/bin/python3
"""Defines unittests for models/amenity.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_two_amenities_unique_ids(self):
        am1a = Amenity()
        am2a = Amenity()
        self.assertNotEqual(am1a.id, am2a.id)

    def test_two_amenities_different_updated_at(self):
        am1a = Amenity()
        sleep(0.05)
        am2a = Amenity()
        self.assertLess(am1a.updated_at, am2a.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        ama = Amenity()
        ama.id = "123456"
        ama.created_at = ama.updated_at = dt
        amstr = ama.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        ama = Amenity()
        sleep(0.05)
        first_updated_at = ama.updated_at
        ama.save()
        second_updated_at = ama.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ama.save()
        self.assertLess(second_updated_at, ama.updated_at)

    def test_save_with_arg(self):
        ama = Amenity()
        with self.assertRaises(TypeError):
            ama.save(None)

    def test_save_updates_file(self):
        ama = Amenity()
        ama.save()
        amid = "Amenity." + ama.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        am = Amenity()
        self.assertIn("id", am.to_dict())
        self.assertIn("created_at", am.to_dict())
        self.assertIn("updated_at", am.to_dict())
        self.assertIn("__class__", am.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ama = Amenity()
        ama.middle_name = "Holberton"
        ama.my_number = 98
        self.assertEqual("Holberton", ama.middle_name)
        self.assertIn("my_number", ama.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ama = Amenity()
        am_dict = ama.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()

