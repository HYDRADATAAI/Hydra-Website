# RECRUITER SCAN AUDIT — W6

## Verdict

`ACCEPTANCE=PASS`

`SCAN_WINDOWS=10s / 30s / 60–90s`

`CONTENT_HIERARCHY=PASS`

`GITHUB_FRONT_DOOR=PASS`

`SCOPE_LABELING=PASS`

`TERMINAL_WALL_RISK=PASS_AFTER_REPAIR`

`BROWSER_RUNTIME_SEAL=DEFERRED_TO_W7`

W6 tests whether a technical recruiter or engineer can understand HYDRA quickly without knowing internal version history. It is an information-hierarchy and recruiter-comprehension pass, not the final browser/deployment QA pass.

## 10-second scan

### Required answer

A visitor should immediately understand:

- what HYDRA is;
- what class of engineering problem it solves;
- which three capabilities define the project;
- that the page will prove those claims rather than continue with marketing copy.

### Locked hero

**HYDRA / MARKET INTELLIGENCE DATA PLATFORM**

**Turn fragmented market data into traceable intelligence.**

`Source-accounted ingestion` · `Contract-bound handoffs` · `Lineage + release gates`

**Result: PASS.**

The hero identifies the project as data engineering, gives a plain-English purpose, and exposes the three core capability families before the visitor scrolls.

## 30-second scan

### What must be visible

A recruiter should encounter three proof ideas quickly:

1. **Real data scale:** 3,353 / 3,353 source records loaded, 0 source errors, 17,766,662 canonical rows written.
2. **Traceability:** replay + reverse trace + lineage proof, explicitly labeled synthetic/shadow.
3. **Failure discipline:** missing authority remains blocked rather than receiving invented semantic values.

### Initial finding

The proof existed, but the strongest evidence was distributed across eight cards. That is defensible for a deep read but slower than necessary for a recruiter scan.

### Repair

Added a three-cell fast proof row ahead of the detailed W2 cards:

`REAL DATA` · `TRACE` · `FAIL CLOSED`

The detailed eight-step proof loop remains unchanged underneath.

**Result: PASS AFTER BOUNDED REPAIR.**

## 60–90-second scan

### What must be understood

The visitor should be able to follow one end-to-end story:

`fragmented evidence → normalization → identity → authority → provenance → interpretation → auditable result`

and understand why HYDRA distinguishes:

`SUPPORTED: LOCAL BOTTLENECK`

from:

`NOT AUTHORIZED: SYSTEMIC SHORTAGE`

### Initial finding

The case was technically clear, but the supported vs. blocked conclusion appeared too late for a fast reader.

### Repair

Added a recruiter fast-read strip immediately after the case question. The full seven-stage case remains below it.

The final representative JSON was also reduced to the fields required to understand the result and its boundary, preventing the output example from becoming a mini log wall.

**Result: PASS AFTER BOUNDED REPAIR.**

## GitHub scan

### Required behavior

A recruiter arriving from LinkedIn or the website should see the same proof vocabulary without first reading repository archaeology.

### Initial finding

The strongest proof table existed, but the README placed architecture and descriptive bullets before the fastest evidence path.

### Repair

Added a `30-second proof` block directly after the project introduction:

- REAL DATA
- TRACE
- FAIL CLOSED

The architecture and deeper proof sections remain intact below.

**Result: PASS AFTER BOUNDED REPAIR.**

## Readability repair

W2 included several 8px scope/status labels. Those labels carry important evidence-scope meaning and should not be the smallest thing on the page.

They were raised to at least 9px in the W6 patched surface.

**Result: PASS.**

## What W6 deliberately did not do

W6 did **not**:

- redesign the frozen hero;
- add decorative screenshots;
- create a fake public runner;
- change evidence scope;
- remove REAL / SYNTHETIC / SHADOW / REPRESENTATIVE labels;
- claim production deployment;
- claim production ML;
- reopen architecture;
- perform the final browser/responsive/deployment seal.

Those runtime/browser checks belong to W7.

## Machine validation

`CHECKS_TOTAL=26`

`CHECKS_PASSED=26`

`CHECKS_FAILED=0`

Validated:

- W2/W3 stylesheet presence;
- bounded word counts;
- no oversized terminal-style preformatted wall in the recruiter path;
- eight-step W2 engineering loop retained;
- W2 fast proof row present;
- W3 seven-stage case retained;
- W3 supported + not-authorized states visible early;
- representative/non-live label retained;
- GitHub 30-second proof occurs before architecture;
- GitHub local Markdown links resolve inside the package;
- public production runner remains explicitly unclaimed;
- hero copy contract retains the approved positioning.

## Acceptance

A recruiter can now understand HYDRA in layers:

**10 seconds:** what it is.

**30 seconds:** what proves it.

**60–90 seconds:** how the engineering behaves when evidence is insufficient.

**PASS W6.**
