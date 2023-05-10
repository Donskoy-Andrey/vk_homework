import unittest
from unittest import mock
from descriptors import Data


class TestDescriptor(unittest.TestCase):
    def test_correct_init(self):
        try:
            cls = Data(num=3, name="yoghurt", price=12)
        except ValueError:
            self.fail("Value error. Incorrect arguments.")

    def test_arguments(self):
        cls = Data(num=3, name="yoghurt", price=12)
        self.assertEqual(cls.num, 3)
        self.assertEqual(cls.name, "yoghurt")
        self.assertEqual(cls.price, 12)

    def test_arguments_type(self):
        cls = Data(num=3, name="yoghurt", price=12)
        self.assertIsInstance(cls.num, int)
        self.assertIsInstance(cls.name, str)
        self.assertIsInstance(cls.price, int)

    def test_num(self):
        with self.assertRaises(ValueError) as error:
            cls = Data(num="3", name="yoghurt", price=12)
        self.assertEqual(error.exception.args, ("The value is not an integer.", ))

    def test_name(self):
        with self.assertRaises(ValueError) as error:
            cls = Data(num=3, name=123, price=12)
        self.assertEqual(error.exception.args, ("The value is not a string.",))

    def test_price(self):
        with self.assertRaises(ValueError) as error:
            cls = Data(num=3, name="yoghurt", price=-12)
        self.assertEqual(error.exception.args, ("The value is not a positive integer.",))

    def test_delete_method(self):
        with mock.patch("descriptors.delattr") as mocker:
            cls = Data(num=3, name="yoghurt", price=12)

            del cls.num
            del cls.name
            del cls.price

            self.assertEqual(mocker.call_count, 3)

        cls = Data(num=3, name="yoghurt", price=12)
        del cls.num
        del cls.name
        del cls.price

        self.assertIsNone(cls.num)
        self.assertIsNone(cls.name)
        self.assertIsNone(cls.price)

    def test_change_to_valid(self):
        try:
            cls = Data(num=3, name="yoghurt", price=12)
            cls.num = 5
            cls.name = "bread"
            cls.price = 100
        except ValueError:
            self.fail("Value error. Incorrect arguments.")

        self.assertEqual(cls.num, 5)
        self.assertEqual(cls.name, "bread")
        self.assertEqual(cls.price, 100)

    def test_change_to_invalid(self):
        cls = Data(num=3, name="yoghurt", price=12)

        with self.assertRaises(ValueError) as error:
            cls.num = "1"
        self.assertEqual(error.exception.args, ("The value is not an integer.",))

        with self.assertRaises(ValueError) as error:
            cls.name = 1001
        self.assertEqual(error.exception.args, ("The value is not a string.",))

        with self.assertRaises(ValueError) as error:
            cls.price = -100
        self.assertEqual(error.exception.args, ("The value is not a positive integer.",))

        self.assertEqual(cls.num, 3)
        self.assertEqual(cls.name, "yoghurt")
        self.assertEqual(cls.price, 12)
