# HYDRA_RECRUITER_PROOF_STRIP_V001

## W2 status

`PASS_W2_BUILD`

This package creates the 30–90 second recruiter proof strip from the W1 public-proof authority map.

## What changed

The strip exposes eight engineering moments:

1. synthetic hostile input
2. controlled / representative handling boundary
3. explicit authority contract
4. source-to-gate trace
5. validation receipt
6. preserved defect
7. defect-scoped repair + rerun
8. blocked authority outcome

## Critical truth controls

- No live/production ingestion claim was introduced.
- No live end-to-end normalization claim was introduced.
- `Contract-bound handoffs` was not used as a blanket claim.
- Shadow evidence is labeled `SHADOW`.
- Synthetic evidence is labeled `SYNTHETIC`.
- The representative transformation card explicitly says public execution proof is pending.
- CI-008 is presented as an authority blocker, not a successful T5→T6 handoff.
- No representative final Constraint output was fabricated.
- The final card treats the blocked state as the verified output.

## Recruiter scan intent

The reader should understand in under 90 seconds that HYDRA demonstrates:

- contract checking;
- source authority;
- lineage;
- release gating;
- deterministic validation;
- defect discovery;
- minimum repair;
- rerun proof;
- refusal to fabricate missing authority.

## Integration

Use `proof-strip-component.html` + `proof-strip.css` to insert the section into the existing HYDRA site.
`index.html` is a standalone preview.

## Next pass

W3 should build the Constraint Case Study V2 using only a receipt-backed public-safe case.
