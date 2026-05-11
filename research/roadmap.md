# Research Roadmap (Refined)

## Project Snapshot
Current implementation provides:
- exact reversible encoding `A(x,y,z) -> (I(x,y), V_i(z))`
- dictionary deduplication of repeated z-vectors
- decompression support (list and NumPy pathways)
- basic functional tests for roundtrip and deduplication

Current gaps:
- no input validation for non-rectangular tensors and invalid indices
- no benchmark harness or baselines
- no quantitative quality metrics beyond deduplication count
- no experiments documented as reproducible protocols

---

## Phase 1 — Stabilization & Reproducibility

### 1.1 Correctness hardening
- Add validation for shape consistency (`X,Y,Z` regularity)
- Define behavior for edge cases:
  - empty tensor
  - empty z-vectors
  - malformed index tables
- Add explicit error types/messages

**Exit criteria**
- 95%+ test coverage for `src/holographic_tensor.py`
- deterministic failure modes for invalid inputs

### 1.2 Test architecture
- Parameterized tests over:
  - varying `(X,Y,Z)` sizes
  - high/low redundancy tensors
  - random seeds for synthetic data
- Property-based tests (Hypothesis):
  - `decompress(compress(T)) == T`
  - index table uniqueness invariant

**Exit criteria**
- automated test matrix in CI
- fixed seed policy documented

### 1.3 Experiment reproducibility
- Add `experiments/` layout:
  - `configs/` (YAML/JSON experiment specs)
  - `scripts/` (benchmark runners)
  - `results/` (versioned outputs)
- Log environment metadata (Python, NumPy, CPU)

**Exit criteria**
- one-command rerun of baseline experiments

---

## Phase 2 — Compression Research (Quantitative)

### 2.1 Baselines and fairness
Compare against:
- lossless general compressors (`gzip`, `lz4`, optionally `zstd`)
- simple tensor-specific baselines (run-length, block dictionary)

Fairness protocol:
- identical serialized input format
- same hardware class and repeated runs
- report mean + std

### 2.2 Core metrics
Track:
- compression ratio (raw/compressed bytes)
- encode/decode latency
- peak memory usage
- table cardinality and index entropy

### 2.3 Synthetic data families
- iid random tensors (control)
- periodic/wave patterns
- block-structured tensors
- sparse-event tensors

**Exit criteria**
- benchmark report with confidence intervals
- scalability curves versus `X*Y*Z` and redundancy level

---

## Phase 3 — Structural & Information Analysis

### 3.1 Entropy study
- Measure entropy of:
  - original tensor stream
  - index map `I(x,y)`
  - basis table distribution
- Estimate regime where projection gives net gains

### 3.2 Scaling laws
Fit empirical models:
- compression ratio as function of redundancy `r`
- runtime as function of `X,Y,Z` and table size `|V|`

### 3.3 Failure regime mapping
Identify where method underperforms:
- near-random tensors
- high unique z-vector density

**Exit criteria**
- documented phase diagram: “helpful vs harmful” data regimes

---

## Phase 4 — Advanced Encoding Variants

### 4.1 Sparse-aware variant
- coordinate compression for mostly-zero z-vectors
- hybrid dense/sparse table mode

### 4.2 Boundary-only / partial reconstruction
- encode boundary slices or selected regions-of-interest
- quantify reconstruction error if lossy variants are introduced

### 4.3 Predictive dictionary growth
- predictive insertion policies for z-vectors
- optional quantized/approximate matching mode (clearly separated as lossy)

**Exit criteria**
- ablation study across variants with shared evaluation protocol

---

## Phase 5 — Visualization & Interpretability

- index-surface heatmaps
- table reuse maps (which `V_i` dominates where)
- scaling plots and Pareto frontiers (ratio vs latency)

**Exit criteria**
- reproducible figures generated directly from experiment artifacts

---

## Phase 6 — Publication Readiness

- Draft paper sections aligned with experiment outputs:
  1. Method
  2. Theoretical framing (information-theoretic analogue)
  3. Experimental protocol
  4. Results and limitations
- Add explicit non-claims section (no physical holographic-principle proof)
- Release open benchmark kit and dataset generators

**Exit criteria**
- arXiv-ready manuscript + public reproducibility package

---

## Priority Backlog (next 2–3 sprints)
1. Input validation + edge-case tests
2. Benchmark harness (`gzip/lz4`) and metric logger
3. Synthetic dataset generator with fixed seeds
4. Entropy and scaling analysis notebook
5. Figure generation pipeline
