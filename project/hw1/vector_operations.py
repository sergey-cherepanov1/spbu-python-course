"""
Implementation of vector operations: dot product,
length calculation, angle between vectors.

"""

from math import acos, pi


def dot_product(vector_1: list[float], vector_2: list[float]) -> float:
    """
    Calculates the dot product of vectors.

    Args:
        vector_1: First vector
        vector_2: Second vector

    Returns:
        Dot product of the given vectors

    Raises:
        ValueError: If vectors have different sizes

    """
    if len(vector_1) != len(vector_2):
        raise ValueError("Vectors sizes must be equal")

    return sum([vector_1[i] * vector_2[i] for i in range(len(vector_1))])


def length(vector: list[float]) -> float:
    """
    Caculates the length of a vector.

    Args:
        vector: Vector

    Returns:
        Size of given vector
    """

    return sum([i**2 for i in vector]) ** 0.5


def angle(vector_1: list[float], vector_2: list[float]) -> float:
    """
    Calculates the angle between two vectors.

    Args:
        vector_1: First vector
        vector_2: Second vector

    Returns:
        Angle between given vectors

    Raises:
        ValueError: If vectors have different sizes

    """
    if len(vector_1) != len(vector_2):
        raise ValueError("Vectors sizes must be equal")

    return (
        180
        * acos(dot_product(vector_1, vector_2) / (length(vector_1) * length(vector_2)))
        / pi
    )
