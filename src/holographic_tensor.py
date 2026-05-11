
from typing import Tuple, List, Any


def _try_import_numpy():
    try:
        import numpy as np
        return np
    except ImportError:
        return None


def compress_3d_to_2d(arr) -> Tuple[List[List[int]], List[Any]]:
    np = _try_import_numpy()

    if np is not None and isinstance(arr, np.ndarray):
        X, Y, Z = arr.shape
        arr_data = arr
    else:
        X = len(arr)
        if X == 0:
            return ([], [])
        Y = len(arr[0])
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
    np = _try_import_numpy()

    X = len(compressed_2d)
    if X == 0:
        return []

    Y = len(compressed_2d[0])

    if len(index_table) > 0:
        Z = len(index_table[0])
    else:
        Z = 0

    result = [[[0 for _ in range(Z)] for _ in range(Y)] for _ in range(X)]

    for x in range(X):
        for y in range(Y):
            idx = compressed_2d[x][y]
            result[x][y] = list(index_table[idx])

    return result
