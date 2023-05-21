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
    def __init__(self, limit: int = 42, logger=None):
        self.limit = limit
        self.storage = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.logger_to_file = logger[0]
        self.logger_to_stdout = logger[1]


    def get(self, key: Hashable):
        """
        Get value from cache.
        """
        if key not in self.storage:
            if self.logger_to_file:
                self.logger_to_file.warn("[get] : Key %s is not in cache.", key)
            if self.logger_to_stdout:
                self.logger_to_stdout.warn("[get] : Key %s is not in cache.", key)
            return None

        node = self.storage[key]
        self.remove_node(node)
        self.add_node(node)
        if self.logger_to_file:
            self.logger_to_file.debug("[get] : Get value by key (%s) from cache", key)
        if self.logger_to_stdout:
            self.logger_to_stdout.debug("[get] : Get value by key (%s) from cache", key)
        return node.value

    def set(self, key: Hashable, value: Any):
        """
        Set value into cache.
        """
        if not isinstance(key, Hashable):
            if self.logger_to_file:
                self.logger_to_file.error(
                    "[set] : Key %s has unhashable type (%s)", key, type(key)
                )
            if self.logger_to_stdout:
                self.logger_to_stdout.error(
                    "[set] : Key %s has unhashable type (%s)", key, type(key)
                )
            raise TypeError(f"unhashable type: '{type(key)}'")

        if key in self.storage:
            if self.logger_to_file:
                self.logger_to_file.debug("[set] : Value by key %s is in cache.", key)
            if self.logger_to_stdout:
                self.logger_to_stdout.debug("[set] : Value by key %s is in cache.", key)
            node = self.storage[key]
            node.value = value
            self.remove_node(node)
            self.add_node(node)
        else:
            if self.logger_to_file:
                self.logger_to_file.debug("[set] : Value by key %s is not in cache.", key)
            if self.logger_to_stdout:
                self.logger_to_stdout.debug("[set] : Value by key %s is not in cache.", key)
            if len(self.storage) >= self.limit:
                if self.logger_to_file:
                    self.logger_to_file.info(
                        "[set] : Storage of cache is full. "
                        "Remove last used element '%s'.",
                        self.tail.prev.key
                    )
                if self.logger_to_stdout:
                    self.logger_to_stdout.info(
                        "[set] : Storage of cache is full. "
                        "Remove last used element '%s'.",
                        self.tail.prev.key
                    )
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
