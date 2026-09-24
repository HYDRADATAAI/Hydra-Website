# Repository map

## 30-second path

Read:

1. [`../README.md`](../README.md)
2. [`TECHNICAL_PROOF.md`](TECHNICAL_PROOF.md)
3. the four compact receipts in [`../evidence/`](../evidence/)

That is enough to understand what HYDRA is, what engineering areas it demonstrates, and how it treats failures.

## 2-minute path

Continue with:

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`CONSTRAINT_CASE.md`](CONSTRAINT_CASE.md)
- [`REAL_VS_SYNTHETIC.md`](REAL_VS_SYNTHETIC.md)

This path answers the common engineering-manager questions: architecture, data quality, provenance, test behavior, and evidence scope.

## Deeper engineer path

The public repository should next expose only a **curated** selection of:

- schema/contract examples;
- normalization/transformation code;
- lineage helpers;
- validation tests;
- defect and rerun receipts;
- representative outputs;
- one safe runnable/demo path if and when independently verified.

Do not make the reader traverse:

- hundreds of historical ZIPs;
- internal batch factories;
- superseded version directories;
- stale handoffs;
- old repair archaeology;
- private/raw source dumps.

## Installation boundary

This package defines the recruiter-facing front door only. It does **not** claim to map the current private `D:\HYDRA` tree, because that authoritative host tree was not inspected during this packaging pass.

When installing into the real repository, link only to source paths that are verified to exist in the current public-safe checkout.
