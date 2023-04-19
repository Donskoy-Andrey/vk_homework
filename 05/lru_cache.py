from typing import Any
from collections.abc import Hashable


class Node:
    def __init__(
            self,
            key: Hashable = None,
            value: Any = None
    ):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit: int = 42):
        self.limit = limit
        self.storage = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: Hashable):
        """
        Get value from cache.
        """
        if key not in self.storage:
            return None

        node = self.storage[key]
        self.remove_node(node)
        self.add_node(node)
        return node.value

    def set(self, key: Hashable, value: Any):
        """
        Set value into cache.
        """
        if not isinstance(key, Hashable):
            raise TypeError(f"unhashable type: '{type(key)}'")

        if key in self.storage:
            node = self.storage[key]
            node.value = value
            self.remove_node(node)
            self.add_node(node)
        else:
            if len(self.storage) >= self.limit:
                del self.storage[self.tail.prev.key]
                self.remove_node(self.tail.prev)
            node = Node(key, value)
            self.storage[key] = node
            self.add_node(node)

    @staticmethod
    def remove_node(node: Node):
        """
        Remove node from any position at the queue.
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def add_node(self, node: Node):
        """
        Add node at the first position at the queue.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
