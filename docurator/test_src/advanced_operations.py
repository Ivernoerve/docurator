"""
Kindly generatoed by GPT
advanced_operations.py

This module provides more advanced operations, such as solving a quadratic equation,
finding the Fibonacci sequence up to a given number, and implementing a custom cache class.
"""
import math
from typing import List, Optional
from docurator import document_me


def solve_quadratic(a: float, b: float, c: float) -> Optional[List[float]]:
    """Solve a quadratic equation of the form ax^2 + bx + c = 0.

    This function returns the real roots of the quadratic equation using the quadratic formula.
    If no real roots exist, None is returned.

    Args:
        a (float): The coefficient of x^2.
        b (float): The coefficient of x.
        c (float): The constant term.

    Returns:
        Optional[List[float]]: A list containing the real roots of the equation, if they exist. Returns None if no real roots exist.

    Raises:
        ValueError: If the coefficient 'a' is zero, which would make it not a quadratic equation.

    Examples:
        >>> solve_quadratic(1, -3, 2)
        [2.0, 1.0]

        >>> solve_quadratic(1, 2, 5)
        None
    """
    if a == 0:
        raise ValueError("'a' must not be zero for a quadratic equation.")

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return [root1, root2]

@document_me
def fibonacci_sequence(n: int) -> List[int]:
    """Generate a list containing the Fibonacci sequence up to the nth term.

    The Fibonacci sequence is a series of numbers in which each number is the sum
    of the two preceding ones, usually starting with 0 and 1.

    Args:
        n (int): The number of terms to generate.

    Returns:
        List[int]: A list containing the first 'n' terms of the Fibonacci sequence.

    Raises:
        ValueError: If 'n' is less than or equal to 0.

    Examples:
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3]

        >>> fibonacci_sequence(1)
        [0]
    """
    if n <= 0:
        raise ValueError("'n' must be greater than 0.")

    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


@document_me
class Cache:
    """A simple cache to store and retrieve values based on keys.

    This cache uses a dictionary internally to store key-value pairs and provides
    methods to add, retrieve, and clear the cache.
    """
    def __init__(self):
        """Initialize an empty cache."""
        self._store = {}

    @document_me
    def add(self, key: str, value: any) -> None:
        """Add a value to the cache with a specific key.

        Args:
            key (str): The key under which the value is stored.
            value (any): The value to store in the cache.

        Examples:
            >>> cache = Cache()
            >>> cache.add('a', 100)
            >>> cache.retrieve('a')
            100
        """
        self._store[key] = value

    @document_me
    def retrieve(self, key: str) -> Optional[any]:
        """Retrieve a value from the cache by its key.

        Args:
            key (str): The key for which the value is to be retrieved.

        Returns:
            Optional[any]: The value associated with the given key, or None if the key is not found.

        Examples:
            >>> cache = Cache()
            >>> cache.add('a', 100)
            >>> cache.retrieve('a')
            100

            >>> cache.retrieve('b')  # Key not found
            None
        """
        return self._store.get(key)

    @document_me
    def clear(self) -> None:
        """Clear all entries from the cache.

        Examples:
            >>> cache = Cache()
            >>> cache.add('a', 100)
            >>> cache.clear()
            >>> cache.retrieve('a')
            None
        """
        self._store.clear()
