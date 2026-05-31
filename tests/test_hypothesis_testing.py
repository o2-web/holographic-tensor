from src.hypothesis_testing import (
    exact_deduplication_metrics,
    repeated_profile_tensor,
    unique_profile_tensor,
)


def test_h1_repeated_profiles_have_clear_structural_gain():
    tensor = repeated_profile_tensor(x_size=8, y_size=8, z_size=16)

    metrics = exact_deduplication_metrics(tensor)

    assert metrics.table_cardinality == 1
    assert metrics.table_cardinality_fraction == 1 / 64
    assert metrics.raw_units == 1024
    assert metrics.encoded_units == 80
    assert metrics.compression_ratio >= 1.5


def test_h1_unique_profiles_are_a_negative_control():
    tensor = unique_profile_tensor(x_size=8, y_size=8, z_size=16)

    metrics = exact_deduplication_metrics(tensor)

    assert metrics.table_cardinality == 64
    assert metrics.table_cardinality_fraction == 1.0
    assert metrics.raw_units == 1024
    assert metrics.encoded_units == 1088
    assert metrics.compression_ratio < 1.0
