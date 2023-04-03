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

    def test_different_thresholds(self) -> None:
        import numpy as np

        for bad_threshold in np.arange(0.1, 0.6, 0.1):
            self.assertEqual(
                predict_message_mood(
                    self.text, self.model,
                    bad_thresholds=bad_threshold, good_thresholds=1.0
                ),
                "норм"
            )

        for good_threshold in np.arange(1, 1.6, 0.1):
            self.assertEqual(
                predict_message_mood(
                    self.text, self.model,
                    bad_thresholds=0.1, good_thresholds=good_threshold
                ),
                "норм"
            )

        for bad_threshold in np.arange(0.9, 1.5, 0.1):
            self.assertEqual(
                predict_message_mood(
                    self.text, self.model,
                    bad_thresholds=bad_threshold, good_thresholds=3.0
                ),
                "неуд"
            )

        for good_threshold in np.arange(0.8, 0.3, -0.1):
            self.assertEqual(
                predict_message_mood(
                    self.text, self.model,
                    bad_thresholds=0.1, good_thresholds=good_threshold
                ),
                "отл"
            )

        same_threshold = self.model.predict(self.text)
        self.assertEqual(
            predict_message_mood(
                self.text, self.model,
                bad_thresholds=same_threshold, good_thresholds=same_threshold
            ),
            "норм"
        )

    @patch("predictor.SomeModel.predict")
    def test_all_variant_of_answers(self, mock):
        mock.side_effect = [i * 0.1 for i in range(0, 14, 2)]
        results = ["неуд", "неуд", "норм", "норм", "норм", "отл", "отл"]

        for result in results:
            self.assertEqual(
                predict_message_mood(
                    self.text, self.model
                ), result
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
