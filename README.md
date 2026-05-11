
# Holographic Tensor Compression

A small experimental research project exploring reversible dimensional reduction of 3D tensors into a 2D indexed representation.

## Concept

The project demonstrates a computational analogue of dimensional reduction:

- Original structure:

  A(x, y, z)

- Compressed representation:

  (I(x, y), V_i(z))

Where:

- `I(x, y)` is a 2D index map
- `V_i(z)` is a table of unique z-vectors

The approach preserves reversibility while reducing redundant storage when many z-vectors repeat.

---

## Main Idea

Instead of storing every `(x, y, z)` value independently:

1. Each `(x, y)` position references a unique z-vector
2. Duplicate z-vectors are stored only once
3. The 3D tensor becomes:
   - a 2D index surface
   - plus a compact basis-state table

This creates an information-preserving dimensional projection.

---

## Features

- Reversible 3D → 2D compression
- Full decompression support
- Dictionary-based tensor deduplication
- NumPy support
- Pytest test suite
- Compression ratio estimation

---

## Project Structure

```

holographic_tensor_project/
├── README.md
├── requirements.txt
├── src/
│   └── holographic_tensor.py
├── tests/
│   └── test_holographic_tensor.py
└── research/
    └── roadmap.md

```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Tests

```bash
pytest
```

---

## Example

```python
from src.holographic_tensor import compress_3d_to_2d

arr = [
    [[1,2,3], [4,5,6]],
    [[1,2,3], [4,5,6]]
]

compressed, table = compress_3d_to_2d(arr)

print(compressed)
print(table)
```

---

## Research Goals

### Near-term
- Benchmark against gzip/lz4
- Add entropy analysis
- Measure scaling laws
- Visualize index surfaces

### Mid-term
- Sparse tensor optimization
- GPU acceleration
- Partial reconstruction experiments
- Boundary-only encoding

### Long-term
- Information-theoretic analysis
- Emergent dimensionality models
- Tensor manifold compression
- Holographic computational analogues

---

## Important Note

This project does NOT claim proof of the physical holographic principle.

Instead, it presents:
- an information-theoretic analogue,
- a reversible dimensional encoding model,
- and an experimental computational framework.

---

## License

MIT
