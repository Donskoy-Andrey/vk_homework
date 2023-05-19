import unittest
import json
import ujson
import cjson


class TestCJson(unittest.TestCase):
    def setUp(self):
        self.json_str = '{"hello": 10, "world": "value"}'

    def test_load_one_item(self):
        try:
            result = cjson.loads('{"key1": "value1"}')
        except ValueError:
            self.fail("Have Exception with load one correct item.")

        self.assertEqual(
            result,
            {"key1": "value1"}
        )

    def test_load_several_items(self):
        try:
            result = cjson.loads(
                '{"key1": "value1", "key2": 123, "key3": "12345"}'
            )
        except ValueError:
            self.fail("Have Exception with load several correct items.")

        self.assertEqual(
            result,
            {"key1": "value1", "key2": 123, "key3": "12345"}
        )

    def test_dump_one_item(self):
        try:
            result = cjson.dumps({"key1": "value1"})
        except ValueError:
            self.fail("Have Exception with dump one correct item.")

        self.assertEqual(
            result,
            '{"key1": "value1"}'
        )

    def test_dump_several_items(self):
        try:
            result = cjson.dumps(
                {"key1": "value1", "key2": 123, "key3": "12345"}
            )
        except ValueError:
            self.fail("Have Exception with dump several correct items.")

        self.assertEqual(
            result,
            '{"key1": "value1", "key2": 123, "key3": "12345"}'
        )

    def test_match(self):
        json_doc = json.loads(self.json_str)
        ujson_doc = ujson.loads(self.json_str)
        cjson_doc = cjson.loads(self.json_str)
        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(json_doc, cjson_doc)

        self.assertEqual(
            self.json_str, cjson.dumps(cjson.loads(self.json_str))
        )