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

## 7. Governed context, lexical retrieval, and structured grounding proof

**Core source:** [`governed-intelligence-sample/`](https://github.com/HYDRADATAAI/Hydra/tree/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample)

**Pinned revision:** [`6dd79a85cdba1f2cd90c2e8815f6d881ac73efad`](https://github.com/HYDRADATAAI/Hydra/commit/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad)

**CI:** [workflow source at the pinned revision](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/.github/workflows/governed-intelligence-sample.yml) and [successful run `37170895042`, attempt 1](https://github.com/HYDRADATAAI/Hydra/actions/runs/37170895042/attempts/1)

**Label:** `SYNTHETIC / NON-LIVE / MODEL NOT EXECUTED`

Demonstrates three bounded repository-controlled flows:

`pipeline manifest -> artifact integrity -> policy decision -> bounded accepted context -> exact citations -> evaluation receipt`

`accepted records -> digest-bound lexical policy -> deterministic ranking -> separately committed qrels, independent of the behavior cases -> Recall@k / MRR receipt`

`governed retrieval -> committed synthetic candidate -> exact claim/value/record/citation checks -> structured-grounding receipt`

Inspectable proof includes:

- [`context.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/context.py) and [`evaluation.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/evaluation.py) for source-byte-bound policies, upstream digest checks, accepted-record context, exact citations, and deterministic context receipts;
- [`retrieval.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/retrieval.py) and [`retrieval_evaluation.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/retrieval_evaluation.py) for accepted-only lexical indexing, integer scoring, deterministic tie breaking, exact citation recomputation, and exact-fraction metric derivation;
- [`retrieval_cases.json`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/fixtures/retrieval_cases.json) for retrieval behavior expectations and separately committed [`retrieval_qrels.json`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/fixtures/retrieval_qrels.json), independent of the behavior cases, for record-level relevance judgments;
- [`grounding.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/grounding.py) and [`grounding_cases.json`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/fixtures/grounding_cases.json) for exact claim, value, record, and citation checks over committed candidate fixtures;
- [`pre_upload_verifier.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/src/hydra_governed_intelligence/pre_upload_verifier.py) and [`test_pre_upload_verifier.py`](https://github.com/HYDRADATAAI/Hydra/blob/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad/governed-intelligence-sample/tests/test_pre_upload_verifier.py) for final receipt verification, independent metric recomputation, fixed ZIP metadata, and byte-identical packaging;
- the pinned workflow and exact successful run, which rebuild, verify, publish, download, and compare the inner proof ZIP digest before reporting success.

Verified retrieval metrics: 13 retrieval cases; 4 `ADMIT` / 6 `ABSTAIN` / 3 `REFUSE`; 0.444444 micro Recall@k; 0.583333 macro Recall@k; 0.666667 MRR.

Verified grounding metrics: 8 grounding cases; 1 `ADMIT` / 5 `QUARANTINE` / 1 `ABSTAIN` / 1 `REFUSE`.

Verified package facts: 9 manifested outputs; 26 receipts; 2 verified input snapshots; 7 independently replayed source rows; 15 bundle members; 41,833 bytes; inner SHA-256 `2b52498e8dfba5f86cf694b08833bbbd67464c91e5cbf6fbd49cd37b1a0698a6`.

The proof bundle includes `source_snapshot.csv` and `resolved_symbol_aliases.json`. The source snapshot contains all seven synthetic rows, including quarantine-designed rows. Governed contexts and receipts remain accepted-only or aggregate-only and do not expose quarantined row payloads.

Candidate responses are committed synthetic fixtures, not model output. Retrieval is lexical, not semantic or embedding retrieval. There is no model or agent execution and no external action. This is repository-controlled evidence, not independent attestation or a trust anchor. It does not establish model quality, natural-language claim extraction, production inference, autonomous analysis, investment advice, or trading authorization.
