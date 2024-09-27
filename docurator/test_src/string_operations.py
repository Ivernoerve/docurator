"""
Kindly generatoed by GPT
string_operations.py

This module provides functions for string manipulation, such as reversing a string, converting to uppercase, and counting vowels.
"""

def reverse_string(s: str) -> str:
    """Reverse the given string.

    Args:
        s (str): The string to be reversed.

    Returns:
        str: The reversed string.
    """
    return s[::-1]

def to_uppercase(s: str) -> str:
    """Convert the given string to uppercase.

    Args:
        s (str): The string to be converted.

    Returns:
        str: The uppercase version of the string.
    """
    return s.upper()

def count_vowels(s: str) -> int:
    """Count the number of vowels in the given string.

    Args:
        s (str): The string in which to count vowels.

    Returns:
        int: The number of vowels in the string.
    """
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)
