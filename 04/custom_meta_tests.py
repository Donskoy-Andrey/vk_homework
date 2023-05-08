from custom_meta import CustomMeta, CustomClass
import unittest


class TestCustomMetaClass(unittest.TestCase):

    def test_call(self):
        class TestClass(metaclass=CustomMeta):
            pass

        cls = TestClass()
        self.assertIsInstance(cls, TestClass)

    def test_new(self):
        class TestClass(metaclass=CustomMeta):
            new_attribute = 1703

        self.assertEqual(TestClass.custom_new_attribute, 1703)


class TestCustomClass(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_class = CustomClass()
        self.another_custom_class = CustomClass(val=900)

    def test_default_init(self):
        self.assertEqual(self.custom_class.custom_val, 99)

    def test_init(self):
        self.assertEqual(self.another_custom_class.custom_val, 900)

    def test_line(self):
        self.assertEqual(self.custom_class.custom_line(), 100)
        self.assertEqual(self.another_custom_class.custom_line(), 100)

        self.assertEqual("custom_line" in self.custom_class.__dir__(), True)
        self.assertEqual("line" in self.custom_class.__dir__(), False)

        self.assertEqual("val" in self.custom_class.__dir__(), False)
        self.assertEqual("custom_val" in self.custom_class.__dir__(), True)

    def test_str(self):
        self.assertEqual(str(self.custom_class), "Custom_by_metaclass")
        self.assertEqual(str(self.another_custom_class), "Custom_by_metaclass")

    def test_new_attributes(self):
        self.custom_class.another_attribute = 123
        self.custom_class.another_attribute_2 = None

        self.assertEqual(self.custom_class.custom_another_attribute, 123)
        self.assertEqual(self.custom_class.custom_another_attribute_2, None)

        self.assertEqual(
            {
                "custom_val": 99,
                "custom_another_attribute": 123,
                "custom_another_attribute_2": None,
            },
            self.custom_class.__dict__
        )