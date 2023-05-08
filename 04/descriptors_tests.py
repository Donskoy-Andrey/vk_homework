import unittest
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
