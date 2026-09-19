# HYDRA Website V7 — Recruiter System + Constraint Case Walkthrough

A dependency-free static project site for HYDRA, positioned as a market-intelligence data engineering platform. V7 adds a recruiter-readable end-to-end case walkthrough without changing the frozen landing-page visual direction.

## Pages

- `index.html` — recruiter-facing overview and system hook
- `architecture.html` — interactive architecture explorer and AWS target mapping
- `constraint.html` — Constraint Intelligence domain model
- `case-study.html` — representative source → identity → contract → evidence → constraint → release walkthrough
- `lab.html` — browser-only integrity/failure-semantics simulation
- `proof.html` — engineering proof, defect discipline, and receipt model
- `roadmap.html` — data → AWS → analytical operations → intelligence roadmap
- `404.html` — custom error page

## Public positioning

The front page remains frozen around:

**HYDRA / MARKET INTELLIGENCE DATA PLATFORM**

**Turn fragmented market data into traceable intelligence.**

V7 deepens the evidence behind that message rather than redesigning the hero.

## Case-study honesty rule

The new end-to-end walkthrough is explicitly labeled as a **representative walkthrough**. It demonstrates HYDRA's intended architecture and data-engineering boundaries without pretending to be live market output or a real trading signal. Replace representative inputs with sanitized real HYDRA artifacts when they are ready for public release.

## Configure public links

Open `site.config.js` and fill only the links that are ready to be public. Empty values remain hidden.

## Preview locally

Run `OPEN_HYDRA_SITE.ps1`, or double-click `index.html`.

## GitHub Pages

The package includes `.github/workflows/pages.yml` and `.nojekyll`. Push the site to a public repository and select **GitHub Actions** as the Pages source.

## Truth rules

1. Current capabilities lead the recruiter-facing story.
2. Future AWS/GenAI work stays in the roadmap until implemented.
3. Browser demonstrations and representative walkthroughs are labeled honestly.
4. No fake production metrics or fabricated authority.
5. Real proof should gradually replace representative surfaces.
6. The landing-page visual direction stays frozen unless a concrete usability issue appears.
