# HYDRA Public Evidence Index

## 1. Repaired integrated seam

**File:** `evidence/CI_TEST_004_PUBLIC_EXCERPT.json`  
**Label:** `SYNTHETIC / SHADOW`

Shows a named cross-thread defect followed by bounded repair and rerun. Publicly relevant facts: rerun PASS, zero failures, baseline immutability preserved, no fabricated mapping claim.

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
**Status:** `SOURCE-ONLY / DORMANT / NOT ACTIVATED`

Pairs the public receipts with a focused implementation example:

- [`authority.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/src/hydra_t6_failclosed/authority.py) validates authority envelope, scope/digest bindings, time validity, revocation/supersession state, and signature trust.
- [`handoff.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/src/hydra_t6_failclosed/handoff.py) validates candidate-only T5→T6 semantics and rejects authority smuggling.
- [`test_camelcase_smuggling.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_camelcase_smuggling.py) provides focused regression coverage for forbidden authority markers and allowed non-authority metadata.

This is inspectable engineering evidence, not a claim that the component is active in a production runtime.
