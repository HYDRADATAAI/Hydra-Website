# HYDRA Public Evidence Index

## 1. Repaired integrated seam

**File:** `evidence/CI_TEST_004_PUBLIC_EXCERPT.json`  
**Label:** `SYNTHETIC / SHADOW`

Shows a named cross-component defect followed by bounded repair and rerun. Publicly relevant facts: rerun PASS, zero failures, baseline immutability preserved, no fabricated mapping claim.

## 2. Quarantine propagation

**File:** `evidence/CI_TEST_006_PUBLIC_EXCERPT.txt`  
**Label:** `SYNTHETIC / SHADOW`

Shows a target expected to quarantine, downstream release blocking, preserved provenance/lineage, reverse-reference checks, and no canonical baseline mutation.

## 3. Authority missing → BLOCK

**File:** `evidence/CI_TEST_008_PUBLIC_EXCERPT.json`  
**Label:** `SHADOW`

Shows that required downstream semantics were not admitted when exact authoritative source ownership was missing. `semantic_values_invented=false`.

## Recruiter takeaway

HYDRA treats correctness, authority, provenance, and blocked states as engineering outcomes that can be tested and inspected.

## 4. Inspectable implementation

**Core source:** [`t6-fail-closed-validator/`](https://github.com/HYDRADATAAI/Hydra/tree/main/t6-fail-closed-validator)  
**CI:** [T6 fail-closed validator](https://github.com/HYDRADATAAI/Hydra/actions/workflows/t6-validator.yml)  
**Status:** `SOURCE-ONLY / DORMANT / NOT ACTIVATED`

Pairs the public receipts with a focused implementation example:

- [`authority.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/src/hydra_t6_failclosed/authority.py) validates authority envelope, scope/digest bindings, time validity, revocation/supersession state, and signature trust.
- [`handoff.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/src/hydra_t6_failclosed/handoff.py) validates candidate-only handoff semantics and rejects authority smuggling.
### Public test suite

- [`test_authority.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_authority.py) covers signed authority acceptance, expiry rejection, and signature tamper rejection.
- [`test_documents.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_documents.py) covers deterministic encoding plus duplicate-key, non-finite-number, and root-shape rejection.
- [`test_receipt.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_receipt.py) covers deterministic inert receipts and rejection of unsafe outcomes.
- [`test_camelcase_smuggling.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_camelcase_smuggling.py) covers forbidden authority markers and allowed non-authority metadata.
- [`test_dormant_adapter.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_dormant_adapter.py) proves the public integration boundary requires dormant readiness and refuses runtime execution.

This is inspectable engineering evidence, not a claim that the component is active in a production runtime.


## 5. Runnable data-engineering pipeline

**Core source:** [`market-data-pipeline-sample/`](https://github.com/HYDRADATAAI/Hydra/tree/main/market-data-pipeline-sample)  
**CI:** [Market data pipeline sample](https://github.com/HYDRADATAAI/Hydra/actions/workflows/market-data-pipeline.yml)  
**Label:** `SYNTHETIC / NON-LIVE`

Demonstrates a compact end-to-end public pipeline:

`CSV → producer contract → normalization → deterministic identity → provenance → quarantine → JSONL / CSV → manifest → checkpointed backfill / recovery receipt`

Inspectable proof includes:

- [`pipeline.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/pipeline.py) for file-level contract enforcement, row normalization, duplicate-event detection, and quarantine;
- [`writers.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/writers.py) for deterministic JSONL, CSV, quarantine, and manifest output;
- [`test_pipeline.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_pipeline.py) for expected 3 accepted / 4 quarantined behavior, deterministic reruns, CSV/JSONL equivalence, provenance, no silent data loss, and contract-drift failure;
- [`test_contract_files.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_contract_files.py) for contract-to-runtime synchronization: input columns, normalized event shape, quarantine shape, and transform-version contract;
- [`operations.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/operations.py) for strict backfill plans, source-byte and partition budgets, atomic checkpoints, integrity-checked reuse, deterministic metrics, and local SLIs;
- [`backfill_plan.json`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/config/backfill_plan.json) for the pinned two-partition synthetic recovery plan;
- [`test_operations.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_operations.py) for interrupted resume, clean/resumed byte equivalence, idempotent replay, tamper rejection, plan drift, row accounting, and budget enforcement;
- the CI workflow, which publishes the generated pipeline and recovery artifacts after injecting an interruption, resuming, and proving a completed replay performs no new source work.

This sample broadens the public evidence from fail-closed authority controls into conventional data-engineering and local operational concerns: ingestion, schema contracts, normalization, identity, lineage/provenance, quarantine, deterministic artifact output, checkpoint recovery, testing, and reproducibility. Its SLIs are synthetic local implementation evidence, not production reliability measurements.

## 6. Runnable SQL data-quality proof

**Core source:** [`sql-data-quality-sample/`](https://github.com/HYDRADATAAI/Hydra/tree/main/sql-data-quality-sample)

**CI:** [SQL data quality sample](https://github.com/HYDRADATAAI/Hydra/actions/workflows/sql-data-quality-sample.yml)

**Label:** `SYNTHETIC / NON-LIVE`

Demonstrates a bounded relational path:

`synthetic CSV -> raw table -> alias join -> normalized view -> quality checks -> accepted/quarantine views -> analytical summary`

Inspectable proof includes:

- [`01_schema.sql`](https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/sql/01_schema.sql) for the raw schema, alias table, normalization join, and deterministic event key;
- [`02_quality.sql`](https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/sql/02_quality.sql) for CTE-based quality classification, `ROW_NUMBER` duplicate detection, and accepted/quarantine views;
- [`03_analytics.sql`](https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/sql/03_analytics.sql) for `LAG`, windowed averages, grouped quality counts, and symbol-level summaries;
- [`run_demo.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/run_demo.py) for deterministic fixture loading and summary generation;
- [`test_sql_sample.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/tests/test_sql_sample.py) for the expected 5 accepted / 3 quarantined behavior, explicit reason codes, alias joins, and analytical regression checks.

This is SQLite-based career evidence for SQL and relational data-quality fundamentals. It is not a claim of a production database, warehouse, distributed query engine, or live feed.
