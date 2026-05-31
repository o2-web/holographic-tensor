"""Utilities for executable checks of research hypotheses.

The helpers in this module intentionally use a simple structural unit model
instead of Python object sizes. A raw tensor stores ``X * Y * Z`` values, while
holographic encoding stores ``X * Y`` indexes plus ``|V| * Z`` table values.
That makes early hypothesis tests deterministic and independent of interpreter
memory overhead.
"""

from dataclasses import dataclass
from typing import List

from src.holographic_tensor import compress_3d_to_2d, decompress_2d_to_3d


Tensor3D = List[List[List[int]]]


@dataclass(frozen=True)
class StructuralCompressionMetrics:
    """Deterministic structural metrics for the exact holographic encoding."""

    x_size: int
    y_size: int
    z_size: int
    table_cardinality: int
    raw_units: int
    index_units: int
    table_units: int

    @property
    def encoded_units(self) -> int:
        """Total structural units in the encoded representation."""
        return self.index_units + self.table_units

    @property
    def compression_ratio(self) -> float:
        """Raw structural units divided by encoded structural units."""
        if self.encoded_units == 0:
            return 1.0
        return self.raw_units / self.encoded_units

    @property
    def table_cardinality_fraction(self) -> float:
        """Share of ``(x, y)`` positions that become unique table entries."""
        positions = self.x_size * self.y_size
        if positions == 0:
            return 0.0
        return self.table_cardinality / positions


def repeated_profile_tensor(x_size: int, y_size: int, z_size: int) -> Tensor3D:
    """Build a tensor where every ``(x, y)`` position shares one z-profile."""
    profile = list(range(z_size))
    return [[list(profile) for _ in range(y_size)] for _ in range(x_size)]


def unique_profile_tensor(x_size: int, y_size: int, z_size: int) -> Tensor3D:
    """Build a tensor where each ``(x, y)`` position has a unique z-profile."""
    return [
        [
            [(x * y_size + y) * z_size + z for z in range(z_size)]
            for y in range(y_size)
        ]
        for x in range(x_size)
    ]


def exact_deduplication_metrics(tensor: Tensor3D) -> StructuralCompressionMetrics:
    """Compress a tensor and return structural metrics for hypothesis checks."""
    compressed, table = compress_3d_to_2d(tensor)
    restored = decompress_2d_to_3d(compressed, table)
    if restored != tensor:
        raise AssertionError("Exact holographic encoding failed to round-trip")

    x_size = len(tensor)
    y_size = len(tensor[0]) if x_size else 0
    z_size = len(tensor[0][0]) if x_size and y_size else 0
    table_cardinality = len(table)

    return StructuralCompressionMetrics(
        x_size=x_size,
        y_size=y_size,
        z_size=z_size,
        table_cardinality=table_cardinality,
        raw_units=x_size * y_size * z_size,
        index_units=x_size * y_size,
        table_units=table_cardinality * z_size,
    )
