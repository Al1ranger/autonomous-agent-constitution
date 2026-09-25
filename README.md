# AutonomousAgentConstitution

An onchain constitutional assembly for small autonomous-agent communities. Members authenticate with their GenLayer transaction sender, cast one immutable ballot per amendment, and can change the charter and future quorum/approval rules only after both mathematical ballot approval and GenLayer semantic guardrail agreement.

This is **not** a certificate, service-delivery verifier, knowledge update, or successor to a protocol-schema upgrade. It does not evaluate external factual claims. The material observations are the contract's current full charter, proposed full charter, fixed founding electorate, and each member's authenticated onchain ballot—not self-reported summaries.

## Why GenLayer

Counts, quorum, one-vote enforcement, and version binding are deterministic. A charter can nevertheless say “every member has one vote” in one clause and grant the founder a unilateral override elsewhere. GenLayer leader and validators independently read both complete charters and assess the same four bounded questions: equal ballots, public record, nonretroactivity, and internal/procedural coherence. Their complete PASS/FAIL/UNKNOWN vector must match exactly. No confidence tolerance can turn a FAIL or UNKNOWN into approval.

## State and consensus

```text
Founder fixes 2–8 addresses + initial charter
  → every invitee explicitly accepts
  → ACTIVE assembly
  → member proposes full replacement charter at exact parent version/hash
  → each authenticated member casts one immutable YES/NO/ABSTAIN ballot
  → quorum + irreversible approval calculation
  → independent GenLayer full-text guardrail assessment
  → RATIFIED / VETOED / INCONCLUSIVE / REJECTED_BALLOT / STALE
```

Only RATIFIED changes the active charter, SHA-256, version, and the numeric quorum/approval thresholds used for later amendments. The hard minimum floors (60% quorum, 66.67% approval) never change. Approval before all votes is possible only if treating every remaining vote as NO still clears the threshold; otherwise the proposal waits. There is no founder veto after formation.

The decision root binds the old/new charter hashes, exact parent version, ordered electorate ballot vector, threshold values, semantic guard vector, outcome, and resulting version. A cross-community amendment or stale parent cannot alter another assembly. Terminal outcomes cannot be reset. No funds are locked; an open proposal may await participation indefinitely.

## Scope

Charters may describe roles, but this release does not execute role permissions or external actions. The binding onchain mechanics are membership, equal ballots, quorum, approval, semantic guardrails, and amendment versioning. It does not prove political fairness, legal validity, or real-world compliance.

## API

`create_community`, `accept_membership`, `activate_community`, `propose_amendment`, `cast_ballot`, `ratify_amendment`, `get_community`, `get_amendment`, `get_ballot`, `get_record`.

## Validate and deploy

```powershell
python -m pip install genvm-linter genlayer-test pytest
genvm-lint check contracts/AutonomousAgentConstitution.py
pytest tests/direct -q
genlayer network set studionet
genlayer deploy --contract contracts/AutonomousAgentConstitution.py
```

Direct tests cover deterministic guards and mocked semantic decisions, not live multi-validator consensus. See `LIVE_PROOFS.md` for finalized deployment and positive/negative ratification transactions. The pinned GenVM runner is declared on the contract's first line.
