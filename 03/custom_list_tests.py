import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_addition(self):
        custom_list1 = CustomList([5, 1, 3, 7])
        custom_list2 = CustomList([1, 2, 7])
        custom_result = CustomList([6, 3, 10, 7])

        self.assertEqual(
            custom_list1 + custom_list2,
            custom_result
        )

        self.assertEqual(
            [*(custom_list1 + custom_list2)],
            [*custom_result]
        )

        self.assertEqual(
            custom_list2 + custom_list1,
            custom_result
        )

        self.assertEqual(
            [*(custom_list2 + custom_list1)],
            [*custom_result]
        )

    def test_addition_with_list(self):
        custom_list1 = CustomList([1])
        custom_list2 = [2, 5]
        custom_result = CustomList([3, 5])

        self.assertEqual(
            custom_list1 + custom_list2,
            custom_result
        )

        self.assertEqual(
            [*(custom_list1 + custom_list2)],
            [*custom_result]
        )

        self.assertEqual(
            custom_list2 + custom_list1,
            custom_result
        )

        self.assertEqual(
            [*(custom_list2 + custom_list1)],
            [*custom_result]
        )

    def test_subtraction(self):
        custom_list1 = CustomList([1])
        custom_list2 = CustomList([2, 4, 5])
        custom_result_1 = CustomList([-1, -4, -5])
        custom_result_2 = CustomList([1, 4, 5])

        self.assertEqual(
            custom_list1 - custom_list2,
            custom_result_1
        )

        self.assertEqual(
            [*(custom_list1 - custom_list2)],
            [*custom_result_1]
        )

        self.assertEqual(
            custom_list2 - custom_list1,
            custom_result_2
        )

        self.assertEqual(
            [*(custom_list2 - custom_list1)],
            [*custom_result_2]
        )

    def test_subtraction_with_list(self):
        custom_list1 = CustomList([1])
        custom_list2 = [2, 5]
        custom_result_1 = CustomList([-1, -5])
        custom_result_2 = CustomList([1, 5])

        self.assertEqual(
            custom_list1 - custom_list2,
            custom_result_1
        )

        self.assertEqual(
            [*(custom_list1 - custom_list2)],
            [*custom_result_1]
        )

        self.assertEqual(
            custom_list2 - custom_list1,
            custom_result_2
        )

        self.assertEqual(
            [*(custom_list2 - custom_list1)],
            [*custom_result_2]
        )

    def test_str(self):
        custom_list = CustomList([1, 2, 3])

        self.assertEqual(
            str(custom_list),
            "Elements: [1, 2, 3], Sum of Elements: 6"
        )

    def test_gt(self):
        custom_list1 = CustomList([1, 2, 4])
        custom_list2 = CustomList([1, 2, 3])

        self.assertEqual(
            custom_list1 > custom_list2,
            True
        )

    def test_ge(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 3])

        self.assertEqual(
            custom_list1 >= custom_list2,
            True
        )

    def test_lt(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 4])

        self.assertEqual(
            custom_list1 < custom_list2,
            True
        )

    def test_le(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 3])

        self.assertEqual(
            custom_list1 <= custom_list2,
            True
        )

    def test_ne(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 4])

        self.assertEqual(
            custom_list1 != custom_list2,
            True
        )
