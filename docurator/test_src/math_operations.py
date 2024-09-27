"""
Kindly generatoed by GPT
math_operations.py

This module provides functions for basic mathematical operations, such as addition, subtraction, multiplication, and division.
"""

def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of the two numbers.
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divide the first number by the second number.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of dividing the first number by the second number.

    Raises:
        ValueError: If the second number is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b
