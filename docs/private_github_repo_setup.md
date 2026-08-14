# Private GitHub Repository Setup

This checklist prepares a new private GitHub repository for the Holographic Tensor Compression project.

## Recommended repository settings

- **Repository name:** `holographic-tensor-lab`
- **Visibility:** Private
- **Default branch:** `main`
- **Description:** Experimental reversible 3D-to-2D tensor compression research toolkit.
- **Topics:** `tensor-compression`, `lossless-compression`, `numpy`, `research`, `holographic-analogue`

## One-command creation with GitHub CLI

> Requires `gh auth login` before running the command.

```bash
gh repo create holographic-tensor-lab \
  --private \
  --description "Experimental reversible 3D-to-2D tensor compression research toolkit" \
  --source . \
  --remote origin \
  --push
```

If the current repository already has an `origin` remote, use a different remote name:

```bash
gh repo create holographic-tensor-lab \
  --private \
  --description "Experimental reversible 3D-to-2D tensor compression research toolkit" \
  --source . \
  --remote private-origin \
  --push
```

## Manual GitHub setup

1. Open GitHub and select **New repository**.
2. Set the repository owner and name to `holographic-tensor-lab`.
3. Select **Private** visibility.
4. Do not initialize with a README, license, or `.gitignore` if pushing this existing project.
5. Create the repository.
6. Add the remote locally:

   ```bash
   git remote add origin git@github.com:<owner>/holographic-tensor-lab.git
   git push -u origin main
   ```

## Suggested protection rules

- Require pull requests before merging into `main`.
- Require status checks to pass before merge.
- Require at least one approval for changes to `src/`, `tests/`, and `research/`.
- Block force-pushes and branch deletion on `main`.
- Enable secret scanning and Dependabot alerts.

## Initial issue backlog

1. Add a benchmark harness with gzip and lz4 baselines.
2. Add synthetic dataset generators with fixed seeds.
3. Add entropy and scaling analysis notebooks.
4. Add visualizations for index surfaces and table reuse maps.
5. Prepare the first reproducible experiment report.
