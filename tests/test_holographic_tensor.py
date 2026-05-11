
from src.holographic_tensor import (
    compress_3d_to_2d,
    decompress_2d_to_3d,
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
