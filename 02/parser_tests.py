import unittest

from unittest import mock
from parser import parse_json
import random


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.base_json = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        self.base_required_fields = ["key1"]
        self.base_keywords = ["word2"]
        self.base_keyword_callback = print

    def test_empty_json_str(self):
        self.assertEqual(
            parse_json(
                required_fields=self.base_required_fields,
                keywords=self.base_keywords,
                keyword_callback=self.base_keyword_callback
            ), None
        )

    def test_empty_required_fields(self):
        self.assertEqual(
            parse_json(
                json_str=self.base_json,
                keywords=self.base_keywords,
                keyword_callback=self.base_keyword_callback
            ), None
        )

    def test_empty_keywords(self):
        self.assertEqual(
            parse_json(
                json_str=self.base_json,
                required_fields=self.base_required_fields,
                keyword_callback=self.base_keyword_callback
            ), None
        )

    def test_empty_keyword_callback(self):
        self.assertEqual(
            parse_json(
                json_str=self.base_json,
                required_fields=self.base_required_fields,
                keywords=self.base_keywords
            ), None
        )

    def test_keyword_callback_count_1(self):
        with mock.patch("parser.print") \
                as mock_keyword_callback:
            parse_json(
                json_str=self.base_json,
                required_fields=self.base_required_fields,
                keywords=self.base_keywords,
                keyword_callback=mock_keyword_callback
            ),

            self.assertEqual(
                mock_keyword_callback.call_count,
                1
            )

    def test_keyword_callback_count_0(self):
        with mock.patch("parser.print") \
                as mock_keyword_callback:
            parse_json(
                json_str="",
                required_fields=self.base_required_fields,
                keywords=self.base_keywords,
                keyword_callback=mock_keyword_callback
            ),

            self.assertEqual(
                mock_keyword_callback.call_count,
                0
            )

    def test_json_Faker(self):

        from faker import Faker
        fake = Faker(locale="Ru_ru")

        results = [
            None,
            ("привлекать", ),
            ("торопливый", )
        ]

        for i, seed in enumerate([1, 13, 42]):
            Faker.seed(seed)
            data = {
                "name": fake.name(),
                "address": fake.address(),
                'company': fake.company(),
                "country": fake.country(),
                'text': fake.sentence(100),
            }
            json_str = "{" + f"\"name\": \"{data['name']}\", " \
                       f"\"address\": \"{data['address']}\"," \
                       f"\"company\": \"{data['company']}\"," \
                       f"\"country\": \"{data['country']}\", " \
                       f"\"text\": \"{data['text']}\"" \
                       + "}"

            random.seed(seed)
            required_fields = random.sample(list(data.keys()), k=3)
            keywords = ["Гвинея", "торопливый", "набор", "привлекать"]
            with mock.patch("parser_tests.print") \
                    as mock_keyword_callback:

                parse_json(
                        json_str=json_str,
                        required_fields=required_fields,
                        keywords=keywords,
                        keyword_callback=mock_keyword_callback
                )
            if mock_keyword_callback.call_count > 0:
                self.assertEqual(
                    mock_keyword_callback.call_args.args,
                    results[i]
                )
            else:
                self.assertEqual(
                    parse_json(
                        json_str=self.base_json,
                        required_fields=self.base_required_fields,
                        keywords=self.base_keywords
                    ), results[i]
                )

