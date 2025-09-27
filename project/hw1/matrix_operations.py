"""
Implementation of matrix operations: addition,
multiplication, matrix transposition.
"""

def check_matrices(matrix_1: list[list[float]], matrix_2: list[list[float]]) -> bool:
    """
    Checks whether the given matrices satisfy the addition conditions.
    Matrices can be added only if they have the same dimensions.
    
    Args:
        matrix_1: First matrix
        matrix_2: Second matrix
    
    Returns:
        True if matrices can be added, False otherwise
    
    """
    
    if len(matrix_1) != len(matrix_2):
        return False
    n = len(matrix_1)
    if len(matrix_1) == 0:
        return False
    if len(matrix_1[0]) != len(matrix_2[0]):
        return False
    m = len(matrix_1[0])
    for i in range(1, n):
        if len(matrix_1[i]) != m or len(matrix_2[i]) != m:
            return False
    return True
    
def add_matrices(matrix_1: list[list[float]], matrix_2: list[list[float]]) -> list[list[float]]:
    """
    Adds matrices.
    
    Args:
        matrix_1: First matrix
        matrix_2: Second matrix
    
    Returns:
        Result of matrix addition
        
    Raises:
        ValueError: If matrices don't satisfy the conditions of addition
    
    """

    if check_matrices(matrix_1, matrix_2):
        n = len(matrix_1)
        return [[matrix_1[i][j] + matrix_2[i][j] for j in range(n)] for i in range(n)]
    raise ValueError("Invalid matrices")

def multiply_matrices(matrix_1: list[list[float]], matrix_2: list[list[float]]) -> list[list[float]]:
    """
    Multiplies matrices.
    
    Args:
        matrix_1: First matrix
        matrix_2: Second matrix
    
    Returns:
        Result of matrix multiplication
        
    Raises:
        ValueError: If the number of columns of the first matrix does not match the number of rows of the second
    """
    
    if len(matrix_1[0]) != len(matrix_2):
        raise ValueError("Invalid matrices")
    n = len(matrix_2)
    m = len(matrix_2[0])
    l = len(matrix_1)
    return [[sum([matrix_1[i][k] * matrix_2[k][j] for k in range(n)]) for j in range(m)] for i in range(l)]

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    """
    Transposes a matrix.
    
    Args:
        matrix: Matrix
    
    Returns:
        Transposed matrix
    """

    n = len(matrix)
    m = len(matrix[0])
    return [[matrix[j][i] for j in range(n)] for i in range(m)]
