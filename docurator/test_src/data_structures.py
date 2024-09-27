"""
Kindly generatoed by GPT
data_structures.py

This module provides classes for custom data structures, such as a stack and a queue.
"""

class Stack:
    """A stack data structure."""

    def __init__(self):
        """Initialize an empty stack."""
        self._items = []

    def push(self, item):
        """Push an item onto the stack.

        Args:
            item: The item to be pushed onto the stack.
        """
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack.

        Returns:
            The top item from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._items:
            raise IndexError("Pop from an empty stack.")
        return self._items.pop()

    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self._items) == 0

class Queue:
    """A queue data structure."""

    def __init__(self):
        """Initialize an empty queue."""
        self._items = []

    def enqueue(self, item):
        """Add an item to the end of the queue.

        Args:
            item: The item to be added to the queue.
        """
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item from the queue.

        Returns:
            The front item from the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if not self._items:
            raise IndexError("Dequeue from an empty queue.")
        return self._items.pop(0)

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self._items) == 0
