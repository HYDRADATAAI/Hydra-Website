# RECRUITER_SCAN_PATH_AUDIT

**Pass:** W6  
**Audit date:** 2026-09-19  
**Mode:** recruiter / engineering-manager / engineer hostile scan  
**Inputs:** frozen recruiter hero + W2 proof-strip structure + W3 constraint case-study structure + W4 GitHub front-door contract + W5 public-claim consistency contract  
**Goal:** make HYDRA understandable in 30 seconds, technically credible in 2 minutes, and inspectable in 5–10 minutes without widening any public claim.

## 1. Final verdict

The recruiter path is materially sound after a small set of bounded information-architecture fixes.

The story now resolves in the correct order:

`WHAT HYDRA IS`
→ `WHAT ENGINEERING IT DEMONSTRATES`
→ `HOW THE DATA FLOWS`
→ `HOW QUALITY / AUTHORITY ARE ENFORCED`
→ `REAL TEST EVIDENCE`
→ `REPRESENTATIVE CONSTRAINT CASE`
→ `GITHUB INSPECTION PATH`

No redesign is required.

### W6 seal

`READER_A_30_SECOND_SCAN=PASS`  
`READER_B_2_MINUTE_SCAN=PASS`  
`READER_C_5_TO_10_MINUTE_SCAN=PASS`  
`HIGH_VALUE_FRICTION_OPEN_AFTER_REMEDIATION=0`  
`UNSUPPORTED_PUBLIC_CLAIMS_INTRODUCED=0`  
`HERO_REDESIGN_REQUIRED=NO`  
`DECORATIVE_REDESIGN_REQUIRED=NO`  
`LIVE_PRODUCTION_IMPLIED=NO`  
`SYNTHETIC_LABELS_PRESERVED=YES`  
`REPRESENTATIVE_LABELS_PRESERVED=YES`

**Boundary:** W6 certifies the recruiter-facing content path and required routing. W7 still owns public deployment, responsive behavior, link integrity, JavaScript errors, overflow, and real rendered navigation.

---

# 2. Reader A — Recruiter, approximately 30 seconds

## Questions

### What is HYDRA?

**PASS**

The opening identity is immediately understandable:

**HYDRA**  
**Market Intelligence Data Platform**

Tagline:

**Turn fragmented market data into traceable intelligence.**

The short explanation must remain bounded to historical/batch data, contracts, authority checks, lineage, and blocked outputs.

### What kind of engineer built it?

**PASS AFTER BOUNDED FIX**

This was the main 30-second friction point.

The existing capability story strongly implies data engineering, but a recruiter should not have to reverse-engineer the job family from architecture vocabulary.

### Required fix

Add one compact line immediately below the hero explanation or at the top of the proof section:

> **Engineering focus: data pipelines, schema/contracts, provenance, validation, deterministic testing, and failure-safe handoffs.**

Do **not** add:
- AWS claims not yet demonstrated here;
- AI Engineer positioning;
- production claims;
- ML-training claims;
- “full-stack” language merely for breadth.

This is a classification aid for the reader, not a new technical claim.

### What technical areas does it demonstrate?

**PASS**

The recruiter should be able to identify these without scrolling deeply:

- historical / batch market-data ingestion;
- normalization and governed structures;
- schema / contract enforcement;
- provenance and lineage;
- deterministic validation / replay;
- defect discovery and bounded repair;
- release / admissibility gates;
- constraint-oriented downstream intelligence structures.

## Reader A path

The first 30 seconds should require only:

1. Hero identity + tagline.
2. Three capability badges.
3. One engineering-focus line.
4. First row of the recruiter proof strip.
5. One clear CTA: **View technical proof**.

### Reader A prohibited friction

Do not place the following before the basic story is understood:

- internal thread names;
- large version numbers;
- giant ZIP inventories;
- T1/T2/T3 archaeology;
- hundreds of test names;
- Baby-ML details;
- CI receipt IDs without a human-readable title.

### Reader A result

`A_WHAT_IS_HYDRA=PASS`  
`A_ENGINEER_TYPE=PASS`  
`A_TECHNICAL_AREAS=PASS`  
`A_INTERNAL_ARCHAEOLOGY_EXPOSED=NO`

---

# 3. Reader B — Engineering manager, approximately 2 minutes

## Can they understand the architecture?

**PASS**

Use the simplified recruiter architecture:

`MARKET / REFERENCE INPUTS`
↓
`INGEST + NORMALIZE`
↓
`IDENTITY / CONTRACT / AUTHORITY CHECKS`
↓
`DATA CORE`
↓
`PROVENANCE + HISTORY / LINEAGE`
↓
`CONSTRAINT / INTELLIGENCE STRUCTURES`
↓
`QUERY / INSPECTION`

Required caption:

> **Logical HYDRA architecture. The diagram shows data flow and tested seams; it does not claim that every edge is live, production-deployed, or authority-cleared.**

Do not show every internal subsystem on this diagram.

## Can they see how data quality is enforced?

**PASS AFTER BOUNDED FIX**

The proof strip should make this explicit through a visible progression:

`INGEST`
→ `NORMALIZE`
→ `CONTRACT`
→ `TRACE`
→ `VALIDATE`
→ `DEFECT`
→ `RESOLUTION / BLOCK`
→ `OUTPUT`

### Required fix

Each proof-strip card needs a one-sentence **engineering purpose**, not merely an artifact snippet.

Example:

- **CONTRACT** — Rejects records that do not satisfy the receiving stage’s governed interface.
- **TRACE** — Preserves where a value came from and how it moved.
- **VALIDATE** — Runs deterministic checks against a bounded seam.
- **BLOCK** — Stops when required authority is missing instead of inventing fields.

This lets a manager understand the system without reading raw receipts.

## Can they understand provenance?

**PASS**

The site must distinguish:

`SOURCE ORIGIN / PROVENANCE`
from
`AUTHORITY / ADMISSIBILITY`
from
`VALIDATION / TEST OUTCOME`

Do not collapse these into a generic “trusted data” badge.

A provenance trail says where something came from.  
An authority gate says whether that source/value is permitted to satisfy a contract.  
A test outcome says whether the bounded behavior passed, failed, or blocked.

That distinction is one of HYDRA’s strongest engineering stories.

## Can they understand testing?

**PASS**

The test section should show three outcomes, not only green cards:

### PASS
A bounded seam behaved as expected.

### FAIL → MINIMUM REPAIR → RERUN
A real defect was identified, corrected within scope, and the same test was rerun.

### BLOCK
Required authority was absent, so the pipeline refused to fabricate a valid-looking result.

The blocked outcome must be presented as a governed result, not hidden as embarrassment.

## Can they inspect real evidence?

**PASS AFTER BOUNDED FIX**

Every major technical proof shown on the website should expose one direct route to the corresponding GitHub evidence.

### Required routing pattern

Human-readable title first:

**Authority gate refused fabricated fields**

Smaller technical metadata underneath:

`CI-TEST-008 · V012 · BLOCKED`

Then:

**Inspect receipt →**

Do not make the engineering manager memorize internal receipt IDs before understanding why the artifact matters.

## Reader B result

`B_ARCHITECTURE=PASS`  
`B_DATA_QUALITY=PASS`  
`B_PROVENANCE=PASS`  
`B_TESTING_MODEL=PASS`  
`B_REAL_EVIDENCE_ROUTE=PASS`

---

# 4. Reader C — Engineer, approximately 5–10 minutes

## Can they find schemas?

**PASS AFTER BOUNDED FIX**

GitHub needs an obvious repository-map entry for:

- schemas / contracts;
- representative governed structures;
- validation rules.

Do not require repository-wide search to locate the first inspectable contract.

## Can they find transformations?

**PASS**

The GitHub front door should identify the inspectable path from:

`source / raw shape`
→ `normalized representation`
→ `contract-bound handoff`

A single small example is better than twenty internal directories.

## Can they find tests?

**PASS**

The Testing section should link a curated set only:

1. one PASS seam receipt;
2. one defect / repaired rerun;
3. one BLOCKED authority receipt.

Do not dump the entire test-result tree on the reader.

## Can they find lineage?

**PASS**

Provide one direct link from the website proof strip and one from GitHub to a lineage / reverse-trace artifact.

The engineer should not have to infer lineage from marketing copy.

## Can they find representative outputs?

**PASS**

The constraint case study is the right landing surface, but it must retain:

> **REPRESENTATIVE EXAMPLE · ARCHITECTURE-FAITHFUL · NOT LIVE MARKET OUTPUT · NOT A TRADING SIGNAL**

The reader should be able to see both:

- a valid structured output shape;
- a rejected / blocked state.

## Can they understand defect handling?

**PASS**

Show the lifecycle:

`TEST`
→ `NAMED DEFECT`
→ `MINIMUM OWNED REPAIR`
→ `SAME TEST RERUN`
→ `PASS OR REMAIN BLOCKED`

This is more valuable than a generic “100% tested” claim.

## Can they run or inspect something?

**PASS AS INSPECTABLE PATH**

Do not manufacture a demo runner merely to make the README look complete.

Until a safe, current, authority-approved public runner exists, the GitHub front door should say:

> **Current public path: inspect architecture, contracts, representative transformations, and named test receipts. A public runnable demo is not claimed here.**

That is preferable to publishing a stale or misleading runtime path.

## Reader C recommended 5–10 minute path

1. `README`
2. `Architecture`
3. `Schemas / contracts`
4. `Representative transformation`
5. `Lineage / provenance example`
6. `PASS receipt`
7. `BLOCKED authority receipt`
8. `Constraint case study`
9. `Repository map`

The full path should be achievable without opening internal archives or version forests.

## Reader C result

`C_SCHEMAS=PASS`  
`C_TRANSFORMATIONS=PASS`  
`C_TESTS=PASS`  
`C_LINEAGE=PASS`  
`C_REPRESENTATIVE_OUTPUTS=PASS`  
`C_DEFECT_HANDLING=PASS`  
`C_RUN_OR_INSPECT_PATH=PASS_INSPECTABLE`

---

# 5. High-value friction found and repaired

## W6-F01 — Engineer identity was too implicit

**Severity:** HIGH  
**Problem:** Recruiter could identify “technical project” but not instantly classify the work as data engineering.  
**Repair:** Add one compact engineering-focus line after the hero explanation.  
**Redesign:** NO.

## W6-F02 — Internal test IDs appeared before human meaning

**Severity:** HIGH  
**Problem:** `CI-TEST-008` means nothing to a first-time reader.  
**Repair:** Human-readable proof title first; technical receipt ID second.  
**Redesign:** NO.

## W6-F03 — PASS cards could dominate the testing story

**Severity:** HIGH  
**Problem:** A wall of green receipts hides HYDRA’s more interesting failure-safety behavior.  
**Repair:** Deliberately show PASS, REPAIRED, and BLOCKED outcomes.  
**Redesign:** NO.

## W6-F04 — Provenance and authority could be mentally collapsed

**Severity:** HIGH  
**Problem:** Reader may think traceable means automatically trusted / admissible.  
**Repair:** Separate `provenance`, `authority`, and `validation` visually and in copy.  
**Redesign:** NO.

## W6-F05 — Architecture arrow risk

**Severity:** HIGH  
**Problem:** A clean diagram can visually imply every edge is live and green.  
**Repair:** Keep the logical-architecture caption; do not render the blocked T5→T6 path as proven live.  
**Redesign:** NO.

## W6-F06 — GitHub could expose the factory floor before the product story

**Severity:** HIGH  
**Problem:** ZIP forests and version archaeology can bury inspectable proof.  
**Repair:** Curated README front door + repository map + three proof receipts.  
**Redesign:** NO.

## W6-F07 — “Run demo” expectation could provoke a fake/stale runner

**Severity:** MEDIUM  
**Problem:** Portfolio conventions can pressure the project to publish a runtime path that is not currently public-safe.  
**Repair:** Explicit inspectable path; no manufactured demo.  
**Redesign:** NO.

## W6-F08 — Representative output could be mistaken for a live market call

**Severity:** HIGH  
**Problem:** Constraint output is visually plausible enough to be misread as current/live intelligence.  
**Repair:** Mandatory representative / non-live / non-signal banner on every surface.  
**Redesign:** NO.

---

# 6. Required website scan order

The public website should preserve this order:

## 01 — Hero

**HYDRA / MARKET INTELLIGENCE DATA PLATFORM**

**Turn fragmented market data into traceable intelligence.**

Badges:

- Historical / batch multi-source ingestion
- Contract-bound handoffs
- Lineage + release gates

Engineering-focus line:

**Data pipelines · schemas/contracts · provenance · validation · deterministic testing · failure-safe handoffs**

## 02 — Architecture

One simplified system diagram.

No giant subsystem census.

## 03 — Recruiter proof strip

`INGEST → NORMALIZE → CONTRACT → TRACE → VALIDATE → DEFECT → RESOLUTION/BLOCK → OUTPUT`

## 04 — Technical proof

Curated evidence cards:

- bounded PASS;
- defect + repaired rerun;
- authority BLOCK.

## 05 — Constraint case study

Source evidence → normalization → governed structure → constraint interpretation → auditable result.

Mandatory representative label.

## 06 — Engineering principles

Explicit authority.  
Deterministic identity where governed.  
Provenance.  
Contract-bound handoffs.  
Testable transformations.  
Blocked rather than fabricated outputs.

## 07 — GitHub / inspect

Clear CTA to curated repository front door.

Do not route the first click to archive archaeology.

---

# 7. Required GitHub scan order

The README should preserve:

1. HYDRA identity + tagline.
2. What it does.
3. Architecture.
4. Data flow.
5. Engineering principles.
6. Technical proof.
7. Representative constraint example.
8. Testing.
9. Real vs synthetic.
10. Repository map.
11. Inspect / demo path.

The first screenful must not lead with:

- hundreds of ZIPs;
- deprecated roots;
- synthetic factories;
- future ML plans;
- giant version trees;
- old `C:\HYDRA` / `_PORTABLE` archaeology.

---

# 8. Copy simplification rules

Use human meaning before internal vocabulary.

### Prefer

**Authority gate blocks unsupported output**  
`CI-TEST-008 · BLOCKED`

### Avoid as the heading

`CI_TEST_008_V012_NO_COMPLETE_PER_FIELD_AUTHORITY_SET`

---

### Prefer

**Cross-stage seam repaired and rerun**  
`CI-TEST-004 · PASS_REPAIRED`

### Avoid as the heading

`V004 CONTROLLED REBASELINE CROSS THREAD...`

---

### Prefer

**Lineage remained stable across deterministic replay**

### Avoid

A paragraph of hashes before the reader knows what was proven.

Hashes belong in evidence detail, not the recruiter headline.

---

# 9. Scan-time budget

## 0–10 seconds

Reader should know:

- project name;
- domain;
- data-engineering orientation;
- core promise.

## 10–30 seconds

Reader should know:

- ingestion;
- contracts;
- lineage;
- validation;
- failure-safe behavior.

## 30–120 seconds

Reader should understand:

- architecture;
- data-quality approach;
- provenance;
- testing;
- one concrete proof.

## 2–10 minutes

Technical reader should be able to inspect:

- one schema;
- one transformation;
- one lineage example;
- one PASS receipt;
- one BLOCK receipt;
- one representative output;
- repository structure.

Anything that does not help one of those windows should not be above the fold merely because it exists.

---

# 10. Do-not-fix list

W6 explicitly does **not** authorize:

- hero redesign;
- typography overhaul;
- color-system changes;
- animation work;
- decorative dashboards;
- fake terminal theatrics;
- additional architecture rings;
- new ML copy;
- broader scale claims;
- new runtime/demo implementation;
- repository reorganization unrelated to the recruiter path;
- polishing internal artifact names for public aesthetics.

The goal is clarity, not cosmetic entropy.

---

# 11. Acceptance

After the bounded fixes above:

`RECRUITER_CAN_IDENTIFY_PROJECT_IN_30_SECONDS=YES`  
`RECRUITER_CAN_IDENTIFY_ENGINEERING_DOMAIN_IN_30_SECONDS=YES`  
`MANAGER_CAN_UNDERSTAND_ARCHITECTURE_IN_2_MINUTES=YES`  
`MANAGER_CAN_FIND_DATA_QUALITY_MODEL=YES`  
`MANAGER_CAN_FIND_PROVENANCE_MODEL=YES`  
`MANAGER_CAN_FIND_TEST_EVIDENCE=YES`  
`ENGINEER_CAN_FIND_SCHEMAS=YES`  
`ENGINEER_CAN_FIND_TRANSFORMATIONS=YES`  
`ENGINEER_CAN_FIND_TESTS=YES`  
`ENGINEER_CAN_FIND_LINEAGE=YES`  
`ENGINEER_CAN_FIND_REPRESENTATIVE_OUTPUT=YES`  
`ENGINEER_CAN_FIND_DEFECT_HANDLING=YES`  
`ENGINEER_HAS_SAFE_INSPECTION_PATH=YES`  
`HIGH_VALUE_FRICTION_OPEN=0`

## Final W6 disposition

`RECRUITER_SCAN_PATH_AUDIT=PASS`

**Next gate:** W7 deployment / responsive / navigation / link seal against the actual rendered public site.
