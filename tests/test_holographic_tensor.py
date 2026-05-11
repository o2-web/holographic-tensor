import pytest

from src.holographic_tensor import (
    compress_3d_to_2d,
    decompress_2d_to_3d,
    TensorValidationError,
)


def test_roundtrip():
    arr = [
        [[1, 2, 3], [4, 5, 6]],
        [[1, 2, 3], [4, 5, 6]]
    ]

    compressed, table = compress_3d_to_2d(arr)
    restored = decompress_2d_to_3d(compressed, table)

    assert restored == arr


def test_deduplication():
    arr = [
        [[1, 1], [1, 1]],
        [[1, 1], [1, 1]]
    ]

    compressed, table = compress_3d_to_2d(arr)

    assert len(table) == 1


def test_empty_tensor_compress():
    compressed, table = compress_3d_to_2d([])
    assert compressed == []
    assert table == []


def test_empty_tensor_decompress():
    restored = decompress_2d_to_3d([], [])
    assert restored == []


def test_non_rectangular_y_rejected():
    arr = [
        [[1, 2]],
        [[1, 2], [3, 4]],
    ]
    with pytest.raises(TensorValidationError, match="rectangular in y"):
        compress_3d_to_2d(arr)


def test_non_rectangular_z_rejected():
    arr = [
        [[1, 2], [3]],
    ]
    with pytest.raises(TensorValidationError, match="rectangular in z"):
        compress_3d_to_2d(arr)


def test_out_of_bounds_index_rejected():
    with pytest.raises(TensorValidationError, match="out of bounds"):
        decompress_2d_to_3d([[1]], [[1, 2, 3]])


def test_non_rectangular_index_map_rejected():
    with pytest.raises(TensorValidationError, match="rectangular"):
        decompress_2d_to_3d([[0], [0, 0]], [[1]])


def test_inconsistent_index_table_rejected():
    with pytest.raises(TensorValidationError, match="uniform length"):
        decompress_2d_to_3d([[0]], [[1], [1, 2]])
