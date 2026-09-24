# Technical proof

This page keeps the public proof set intentionally small. Each item demonstrates a different part of the engineering loop.

## 1. Real canonicalization

A historical options-chain canonicalization run completed with:

```text
overall_status              = PASS
source_records_discovered   = 3,353
source_records_loaded       = 3,353
source_records_error        = 0
unique_symbols_loaded       = 3,353
rows_in_total               = 17,766,662
canonical_rows_written      = 17,766,662
```

Why it matters: this is direct evidence that HYDRA has processed a large real historical source set into a controlled canonical layer rather than existing only as an architecture diagram.

Evidence: [`../evidence/OPTIONS_CANONICALIZATION_RECEIPT.txt`](../evidence/OPTIONS_CANONICALIZATION_RECEIPT.txt)

## 2. Integrated lineage and replay

A bounded cross-thread seam test reported:

```text
T3_EXACT_REPLAY_MATCH       = True
T3_LINEAGE_DIGEST_STABLE    = True
T4_REVERSE_TRACE_COMPLETE   = True
T4_WHY_TRACE_COMPLETE       = True
T5_BLOCKER_IF_UNRESOLVED    = True
SEALED_BATCH60_MUTATED      = NO
OVERALL                     = PASS_FIRST_BEHAVIORAL_CROSS_THREAD_SEAM
```

Why it matters: passing data forward is not enough. The test also proves replay stability, reverse traceability, reason tracing, and unchanged frozen baseline state.

Scope: **SYNTHETIC / SHADOW INTEGRATION**.

Evidence: [`../evidence/CI_TEST_005_LINEAGE_RECEIPT.txt`](../evidence/CI_TEST_005_LINEAGE_RECEIPT.txt)

## 3. Defect-scoped repair and rerun

CI-TEST-004 returned:

```text
OVERALL                         = PASS_REPAIRED_CI_TEST_004
CANONICAL_BASELINE_MUTATED      = NO
FABRICATED_HISTORICAL_MAPPING   = NO
FAILURE_COUNT                   = 0
T1_TO_T2_TO_T3_TO_T4_TO_T5     = PASS
BATCH60_IMMUTABILITY_PIN        = PASS
```

The repair removed an unproven same-family requirement instead of inventing a historical mapping to force green status.

Why it matters: the engineering discipline is **prove defect → minimum repair → rerun**, not “rewrite until the test passes.”

Scope: **SYNTHETIC / SHADOW INTEGRATION**.

Evidence: [`../evidence/CI_TEST_004_REPAIR_RECEIPT.txt`](../evidence/CI_TEST_004_REPAIR_RECEIPT.txt)

## 4. Authority rejection instead of fabrication

A native T5→T6 handoff required these fields:

```text
upstream_object_id
object_type
subject_entity_id
as_of
confidence
evidence_ids
payload
```

The available Batch60 objects could not supply five required semantic fields from authoritative case data. The result remained blocked:

```text
ready_t5_candidate_count = 0
semantic_values_invented = false
overall = FAIL_CI008_V005_T5_NATIVE_MATERIALIZATION_FIELDS_ABSENT
```

Why it matters: **discoverable information is not automatically authorized information**. The pipeline blocks instead of filling required semantic fields from filenames, sequence numbers, unrelated fixtures, or guesses.

Scope: **SYNTHETIC / SHADOW INTEGRATION**.

Evidence: [`../evidence/CI_TEST_008_AUTHORITY_BLOCK.json`](../evidence/CI_TEST_008_AUTHORITY_BLOCK.json)

## What this proof set does not claim

It does not claim live production constraint generation, production ML, automated trading, or a production deployment. Those claims are intentionally absent until equivalent evidence exists.
