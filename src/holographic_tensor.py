from typing import Tuple, List, Any


class TensorValidationError(ValueError):
    """Raised when tensor-like inputs are malformed or inconsistent."""


def _try_import_numpy():
    try:
        import numpy as np
        return np
    except ImportError:
        return None


def _validate_list_tensor(arr):
    if not isinstance(arr, list):
        raise TensorValidationError("Input tensor must be a 3D list or NumPy ndarray")

    X = len(arr)
    if X == 0:
        return 0, 0, 0

    if not all(isinstance(row, list) for row in arr):
        raise TensorValidationError("Tensor must be rectangular: each x-slice must be a list")

    Y = len(arr[0])

    for x, row in enumerate(arr):
        if len(row) != Y:
            raise TensorValidationError(
                f"Tensor must be rectangular in y dimension: row {x} has length {len(row)} expected {Y}"
            )
        for y, z_vector in enumerate(row):
            if not isinstance(z_vector, list):
                raise TensorValidationError(
                    f"Tensor must contain z-vectors as lists: found {type(z_vector).__name__} at ({x}, {y})"
                )

    Z = len(arr[0][0]) if Y > 0 else 0

    for x, row in enumerate(arr):
        for y, z_vector in enumerate(row):
            if len(z_vector) != Z:
                raise TensorValidationError(
                    f"Tensor must be rectangular in z dimension: vector at ({x}, {y}) has length {len(z_vector)} expected {Z}"
                )

    return X, Y, Z


def _validate_decompression_inputs(compressed_2d, index_table):
    if not isinstance(compressed_2d, list):
        raise TensorValidationError("Compressed index map must be a 2D list")
    if not isinstance(index_table, list):
        raise TensorValidationError("Index table must be a list of z-vectors")

    X = len(compressed_2d)
    if X == 0:
        return 0, 0, 0

    if not all(isinstance(row, list) for row in compressed_2d):
        raise TensorValidationError("Compressed index map must be rectangular: each row must be a list")

    Y = len(compressed_2d[0])
    for x, row in enumerate(compressed_2d):
        if len(row) != Y:
            raise TensorValidationError(
                f"Compressed index map must be rectangular: row {x} has length {len(row)} expected {Y}"
            )

    if len(index_table) == 0:
        for x, row in enumerate(compressed_2d):
            for y, idx in enumerate(row):
                if idx != 0:
                    raise TensorValidationError(
                        f"Index table is empty but found non-zero index {idx} at ({x}, {y})"
                    )
        return X, Y, 0

    if not all(isinstance(z_vector, list) for z_vector in index_table):
        raise TensorValidationError("Index table must contain z-vectors as lists")

    Z = len(index_table[0])
    for i, z_vector in enumerate(index_table):
        if len(z_vector) != Z:
            raise TensorValidationError(
                f"Index table z-vectors must have uniform length: vector {i} has length {len(z_vector)} expected {Z}"
            )

    for x, row in enumerate(compressed_2d):
        for y, idx in enumerate(row):
            if not isinstance(idx, int):
                raise TensorValidationError(
                    f"Compressed index must be integer: found {type(idx).__name__} at ({x}, {y})"
                )
            if idx < 0 or idx >= len(index_table):
                raise TensorValidationError(
                    f"Compressed index {idx} out of bounds at ({x}, {y}) for table size {len(index_table)}"
                )

    return X, Y, Z


def compress_3d_to_2d(arr) -> Tuple[List[List[int]], List[Any]]:
    np = _try_import_numpy()

    if np is not None and isinstance(arr, np.ndarray):
        if arr.ndim != 3:
            raise TensorValidationError(f"NumPy tensor must be 3D, got {arr.ndim}D")
        X, Y, _ = arr.shape
        arr_data = arr
    else:
        X, Y, _ = _validate_list_tensor(arr)
        if X == 0:
            return ([], [])
        arr_data = arr

    vector_to_index = {}
    index_table = []

    compressed_2d = [[0 for _ in range(Y)] for _ in range(X)]

    for x in range(X):
        for y in range(Y):
            if np is not None and isinstance(arr_data, np.ndarray):
                z_vector = arr_data[x, y, :].tolist()
            else:
                z_vector = arr_data[x][y]

            vector_key = tuple(z_vector)

            if vector_key not in vector_to_index:
                vector_to_index[vector_key] = len(index_table)
                index_table.append(z_vector)

            compressed_2d[x][y] = vector_to_index[vector_key]

    return compressed_2d, index_table


def decompress_2d_to_3d(compressed_2d, index_table):
    X, Y, Z = _validate_decompression_inputs(compressed_2d, index_table)
    if X == 0:
        return []

    result = [[[0 for _ in range(Z)] for _ in range(Y)] for _ in range(X)]

    for x in range(X):
        for y in range(Y):
            idx = compressed_2d[x][y]
            result[x][y] = list(index_table[idx]) if len(index_table) > 0 else []

    return result
