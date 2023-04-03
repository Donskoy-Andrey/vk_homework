import unittest
from unittest.mock import patch, call
from predictor import SomeModel, predict_message_mood


class TestPredict(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()
        self.text = "Чапаев и пустота"
        self.text_2 = "Чапаев и густота"

    def test_positive(self) -> None:
        self.assertEqual(
            predict_message_mood(self.text, self.model), "отл"
        )

    def test_negative(self) -> None:
        self.assertEqual(
            predict_message_mood("Вулкан", self.model), "неуд"
        )

    def test_normal(self) -> None:
        self.assertEqual(
            predict_message_mood("Булочки и чай", self.model), "норм"
        )

    @patch("predictor.SomeModel.predict")
    def test_boundary(self, mock) -> None:
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

    @patch("predictor.SomeModel.predict")
    def test_predict_message(self, mock) -> None:
        mock.return_value = 1.0

        result_1 = predict_message_mood(self.text, self.model)
        result_2 = predict_message_mood(self.text_2, self.model)

        calls = [call(text) for text in [self.text, self.text_2]]
        self.assertEqual(
            calls,
            mock.call_args_list
        )

    @patch("predictor.SomeModel.predict")
    def test_predict_call_count(self, mock) -> None:
        mock.side_effect = [i for i in range(10)]
        [predict_message_mood(self.text, self.model) for i in range(10)]
        self.assertEqual(mock.call_count, 10)
