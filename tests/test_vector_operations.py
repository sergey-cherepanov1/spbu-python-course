import pytest
from hw1 import vector_operations as vo


def test_dot_product_basic():
    """Basic dot product test."""
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    result = vo.dot_product(v1, v2)
    expected = 32
    assert result == expected


def test_dot_product_different_lengths_error():
    """Error test for different vector lengths."""
    v1 = [1, 2, 3]
    v2 = [1, 2]
    with pytest.raises(ValueError):
        vo.dot_product(v1, v2)


def test_vector_length_basic():
    """Basic length test."""
    assert vo.length([1, 2, 2]) == 3.0


def test_angle_parallel_vectors():
    """Parallel vectors test."""
    v1 = [1, 2]
    v2 = [2, 4]
    assert abs(vo.angle(v1, v2) - 0.0) < 0.00001


def test_angle_orthogonal_vectors():
    """Orthogonal vectors test."""
    v1 = [1, 0]
    v2 = [0, 1]
    assert vo.angle(v1, v2) == 90.0
