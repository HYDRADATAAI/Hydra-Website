# HYDRA_CONSTRAINT_CASE_STUDY_V2

## W3 status

`W3_ACCEPTANCE=PASS`

## Recruiter-facing story

`FRAGMENTED MARKET EVIDENCE`
→ `SOURCE NORMALIZATION`
→ `SOURCE AUTHORITY`
→ `CONTRACT + LINEAGE`
→ `CONSTRAINT INTERPRETATION`
→ `ADMISSIBILITY CHECK`
→ `AUDITABLE RESULT`

The case translates the internal engineering rule into plain language:

**Discoverable data is not automatically authorized data.**

## Truth boundary

The market evidence and displayed semantic object are explicitly `REPRESENTATIVE`.
They are not presented as live HYDRA market outputs.

The receipt-backed controls are labeled separately:

- N4 source-authority behavior: `INTEGRATED`
- CI-006 lineage/quarantine/release-block proof: `SHADOW`
- CI-008 T6/admissibility authority proof: `SHADOW`

## Visible blocked state

The public page shows the real engineering outcome:

- native T6 validator: PASS
- native T6 field contract: PASS
- exact Batch60 T5 binding: FAIL
- authority hits: 0
- complete cases: 0
- nonblocked T5 cases evaluated: 1206
- deterministic double scan: true
- semantic values invented: false
- final state: BLOCKED

No `object_type`, `subject_entity_id`, `as_of`, `confidence`, or `evidence_ids`
are invented to make the case look complete.

## Constraint semantics

The case explains the governed N1 boundary without pretending the displayed
market example is an executed output:

classification may refine an existing authorized Constraint;
classification may not mint canonical existence or identity.

## Public safety

The component omits local drive paths, usernames, raw proprietary sources,
and internal filesystem archaeology.

## Integration

Use:

- `case-study-component.html`
- `case-study.css`

`index.html` is the standalone preview.

Recommended site order:

`RECRUITER HERO`
→ `RECRUITER PROOF STRIP`
→ `CONSTRAINT CASE STUDY V2`
→ deeper architecture / evidence
