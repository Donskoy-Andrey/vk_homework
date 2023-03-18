import unittest
from unittest.mock import patch
from task1 import SomeModel, predict_message_mood


class TestPredict(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()

    def test_positive(self) -> None:
        self.assertEqual(
            predict_message_mood("Чапаев и пустота", self.model), "отл"
        )

    def test_negative(self) -> None:
        self.assertEqual(
            predict_message_mood("Вулкан", self.model), "неуд"
        )

    def test_normal(self) -> None:
        self.assertEqual(
            predict_message_mood("Булочки и чай", self.model), "норм"
        )

    def test_boundary(self) -> None:
        with patch("task1.SomeModel.predict") as mock:
            mock.side_effect = [0.3, 0.8]

            self.assertEqual(
                predict_message_mood(
                    "some text with return value 0.3 (норм)",
                    self.model), "норм"
            )

            self.assertEqual(
                predict_message_mood(
                    "some text with return value 0.8 (норм)",
                    self.model), "норм"
            )
