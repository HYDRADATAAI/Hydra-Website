# HYDRA_RECRUITER_JOURNEY_CTA_V001

## W6 status

`W6_ACCEPTANCE=PASS`

## Purpose

W6 closes the recruiter-facing journey after W2–W5.

The page now provides four deliberate review depths:

1. **30–90 sec** → Recruiter Proof Strip
2. **3–5 min** → Constraint Case Study V2
3. **Technical** → Architecture + Evidence Bridge
4. **Receipts** → Technical Proof Index

The combined preview embeds the actual W2–W5 standalone builds and adds W6 as the closeout/CTA layer.

## External action policy

Exact external destinations were not available to W6.

Therefore:

- GitHub is `UNBOUND`
- LinkedIn is `UNBOUND`
- Contact is `UNBOUND`

W6 does **not** invent URLs or email addresses.

This is an intentional pre-deployment state, not a broken-link workaround.

Before public deployment, the exact external destinations must be supplied and bound.

`EXTERNAL_ACTION_BINDING_REQUIRED_BEFORE_PUBLIC_DEPLOYMENT=YES`

## Internal routing

The W6 internal actions bind to the actual site section IDs:

- `#proof`
- `#constraint-case-study`
- `#architecture-evidence`
- `#technical-proof`

The combined W2–W6 preview contains all four target anchors.

## Frozen hero

W6 does not modify the frozen V1 recruiter hero.

Recommended final journey:

`FROZEN RECRUITER HERO`
→ `W2 RECRUITER PROOF STRIP`
→ `W3 CONSTRAINT CASE STUDY V2`
→ `W4 ARCHITECTURE + EVIDENCE`
→ `W5 TECHNICAL PROOF INDEX`
→ `W6 RECRUITER JOURNEY / CTA`

## W7 handoff

W7 should treat unbound external actions as a deployment preflight blocker if the public release requires them.

W7 should also verify:

- desktop/tablet/mobile;
- internal anchor navigation;
- final external URLs once bound;
- overflow and readability;
- JS errors;
- public deployment routing.
