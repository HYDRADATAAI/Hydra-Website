# Real vs Synthetic / Shadow Boundary

HYDRA's public surfaces use explicit labels so a reader can distinguish what is being demonstrated.

## REPRESENTATIVE

The recruiter-facing market constraint example, illustrative fragmented-source fields, normalized evidence object, identity mapping, constraint interpretation, and final case-study object. These communicate structure and behavior; they are not presented as live production observations.

## SYNTHETIC / NON-LIVE

The Python market-data pipeline and checkpoint-recovery fixtures, the SQLite data-quality fixture, and the governed context, lexical-retrieval, qrel, structured-grounding, receipt, and deterministic-package fixtures. They demonstrate normalization, relational quality checks, quarantine, checkpoint recovery, idempotent replay, citation integrity, accepted-only lexical ranking evaluated against separately committed qrels, independent of the behavior cases, structured claim/value/record/citation checks, and policy decisions using committed synthetic inputs without live operation.

Verified retrieval metrics: 13 retrieval cases; 4 `ADMIT` / 6 `ABSTAIN` / 3 `REFUSE`; 0.444444 micro Recall@k; 0.583333 macro Recall@k; 0.666667 MRR.

Verified grounding metrics: 8 grounding cases; 1 `ADMIT` / 5 `QUARANTINE` / 1 `ABSTAIN` / 1 `REFUSE`.

Verified package facts: 9 manifested outputs; 26 receipts; 2 verified input snapshots; 7 independently replayed source rows; 15 bundle members; 41,833 bytes; inner SHA-256 `2b52498e8dfba5f86cf694b08833bbbd67464c91e5cbf6fbd49cd37b1a0698a6`.

The proof bundle intentionally includes `source_snapshot.csv` and `resolved_symbol_aliases.json` so raw provenance can be independently replayed. The source snapshot contains all seven synthetic rows, including quarantine-designed rows. Governed contexts and receipts remain accepted-only or aggregate-only and do not expose quarantined row payloads.

Proof revision: [`6dd79a85cdba1f2cd90c2e8815f6d881ac73efad`](https://github.com/HYDRADATAAI/Hydra/tree/6dd79a85cdba1f2cd90c2e8815f6d881ac73efad). Successful governed workflow: [attempt 1](https://github.com/HYDRADATAAI/Hydra/actions/runs/37170895042/attempts/1).

Candidate responses are committed synthetic fixtures, not model output. Retrieval is lexical, not semantic or embedding retrieval. There is no model or agent execution and no external action. The workflow is repository-controlled evidence for the pinned revision, not independent attestation or a trust anchor.

## SYNTHETIC / SHADOW

The public CI-004 and CI-006 excerpts and other control-plane validation receipts when explicitly labeled. They demonstrate contract, integration, lineage, quarantine, and release-gate behavior within synthetic/shadow boundaries.

## SHADOW

The CI-008 authority-block example. It demonstrates a fail-closed handoff when authoritative semantic ownership cannot be proven.

## NOT CLAIMED

- live production operation;
- production constraint detection;
- live automated market conclusions;
- a production database, data warehouse, or distributed query platform;
- production SLO attainment, uptime, incident response, or operating cost;
- a deployed orchestration or observability service;
- canonical production promotion;
- production ML training or model execution;
- model quality, semantic or embedding retrieval quality, or natural-language intent classification;
- natural-language claim extraction or generated candidate responses;
- agent execution, broker interaction, or any external action;
- autonomous analysis, investment advice, or trading authorization;
- independent attestation or a trust anchor;
- production runtime availability.

Ambiguous marketing language that could imply any of the above should not be used.
