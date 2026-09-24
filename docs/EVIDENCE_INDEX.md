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
- [`handoff.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/src/hydra_t6_failclosed/handoff.py) validates candidate-only T5→T6 semantics and rejects authority smuggling.
### Public test suite

- [`test_authority.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_authority.py) covers signed authority acceptance, expiry rejection, and signature tamper rejection.
- [`test_documents.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_documents.py) covers deterministic encoding plus duplicate-key, non-finite-number, and root-shape rejection.
- [`test_receipt.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_receipt.py) covers deterministic inert receipts and rejection of unsafe outcomes.
- [`test_camelcase_smuggling.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_camelcase_smuggling.py) covers forbidden authority markers and allowed non-authority metadata.
- [`test_dormant_adapter.py`](https://github.com/HYDRADATAAI/Hydra/blob/main/t6-fail-closed-validator/tests/test_dormant_adapter.py) proves the public integration boundary requires dormant readiness and refuses runtime execution.

This is inspectable engineering evidence, not a claim that the component is active in a production runtime.
