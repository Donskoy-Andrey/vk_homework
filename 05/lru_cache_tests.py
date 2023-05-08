import unittest
from lru_cache import LRUCache, Node


class TestLruCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(2)
        self.cache_limit_one = LRUCache(1)
        self.another_cache = LRUCache()
        self.another_cache.set("existent key 1", 123)
        self.another_cache.set("existent key 2", "text")
        self.another_cache.set("existent key 3", Node)

    def test_init_method(self):
        self.assertEqual(self.cache.__dict__["limit"], 2)
        self.assertEqual(self.cache.__dict__["storage"], {})

        self.assertIsInstance(self.cache.__dict__["head"], Node)
        self.assertIsInstance(self.cache.__dict__["tail"], Node)

    def test_get_set_methods(self):
        self.assertEqual(self.cache.get("non-existent key 1"), None)
        self.assertEqual(self.cache.get("non-existent key 2"), None)
        self.assertEqual(self.cache.get("non-existent key 3"), None)

        self.assertEqual(self.another_cache.get("existent key 1"), 123)
        self.assertEqual(self.another_cache.get("existent key 2"), "text")
        self.assertEqual(self.another_cache.get("existent key 3"), Node)

    def test_remove_node_method(self):
        self.another_cache.remove_node(
            self.another_cache.storage["existent key 2"]
        )

        node_1 = self.another_cache.storage["existent key 3"]
        node_2 = self.another_cache.storage["existent key 1"]

        self.assertEqual(node_1.next, node_2)
        self.assertEqual(node_1, node_2.prev)

    def test_add_node_method(self):
        new_node = Node(value=1010)
        self.another_cache.add_node(new_node)
        self.assertEqual(
            self.another_cache.head.next.value, 1010
        )

        new_node_2 = Node(value="CHECK")
        self.another_cache.add_node(new_node_2)
        self.assertEqual(
            self.another_cache.head.next.value, "CHECK"
        )

    def test_rewriting_storage(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        self.assertEqual(self.cache.get("k3"), None)
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k1"), "val1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "val1")

    def test_rewriting_values(self):
        self.cache.set("k1", "val1")
        self.cache.set("k1", "HelloWorld")

        self.assertEqual(
            self.cache.get("k1"), "HelloWorld"
        )

    def test_unhashable_error(self):
        self.assertRaises(
            TypeError, lambda: self.cache.set(list(), 'value')
        )

    def test_limit_one(self):
        self.cache_limit_one.set("k1", "val1")
        self.cache_limit_one.set("k2", "val2")
        self.cache_limit_one.set("k3", "val3")

        self.assertEqual(
            len(self.cache_limit_one.storage), 1
        )
        self.assertIsNone(
            self.cache_limit_one.get("k1")
        )
        self.assertIsNone(
            self.cache_limit_one.get("k2")
        )
        self.assertEqual(
            self.cache_limit_one.get("k3"), "val3"
        )

    def test_rewrite_existed_value(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k1", "val3")

        self.assertEqual(
            len(self.cache.storage), 2
        )
        self.assertEqual(
            self.cache.get("k1"), "val3"
        )
        self.assertEqual(
            self.cache.get("k2"), "val2"
        )

    def test_change_value(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k1", "new_val1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "new_val1")

    def test_change_order_get(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        _ = self.cache.get("k1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "val1")
