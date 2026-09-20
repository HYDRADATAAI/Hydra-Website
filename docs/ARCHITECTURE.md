# HYDRA Public Architecture

## Purpose

HYDRA's recruiter-facing architecture centers on traceability across data-engineering handoffs. The public story is intentionally narrower than the internal project tree.

## Pipeline

`FRAGMENTED MARKET EVIDENCE → SOURCE NORMALIZATION → IDENTITY RESOLUTION → CONTRACT / AUTHORITY CHECK → PROVENANCE + HISTORY → CONSTRAINT INTERPRETATION → AUDITABLE RESULT`

## Handoff rule

A downstream field is admissible only when an authoritative producer owns it or an existing contract permits its derivation. Merely discovering a plausible value elsewhere does not authorize the handoff.

## Failure behavior

A blocked outcome is valid. When authority cannot be proven, HYDRA is expected to stop, preserve the unresolved state, and avoid fabricated semantics.

## Public claim boundary

The market walkthrough is **REPRESENTATIVE**. The control receipts are **SYNTHETIC / SHADOW** as labeled. This document does not claim a live production runtime.
