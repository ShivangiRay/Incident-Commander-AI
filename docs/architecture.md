# Architecture

## Product Intent

Incident Commander AI is an SRE investigation console. It ingests incident signals, correlates anomalies, ranks hypotheses, estimates blast radius, applies policy gates, recommends mitigations, retrieves similar incidents, and drafts postmortems.

## Assumptions

- This bootstrap uses synthetic OpenTelemetry-like, Prometheus-like, Loki-like, deployment, and runbook records.
- No destructive action is executed. Actions are recommendations with policy decisions and approval states.
- Vector retrieval is represented by deterministic tag/service overlap scoring; production can replace it with pgvector or hybrid search.

## Components

- `apps/api`: FastAPI endpoints for scenario ingestion, investigation runs, policies, recommendations, and postmortems.
- `apps/web`: dashboard for active incidents, timelines, evidence graphs, hypotheses, blast radius, policy decisions, recommended actions, similar incidents, and review console.
- `agents/ingestion`: normalizes raw signals into typed incident signals.
- `agents/correlation`: builds evidence timeline and related anomaly groups.
- `agents/hypothesis`: ranks root-cause hypotheses with supporting and contradictory evidence.
- `agents/blast-radius`: estimates services, regions, endpoints, and dependencies impacted.
- `agents/policy`: classifies action risk and approval requirements.
- `agents/action-recommender`: maps hypotheses to mitigations and runbooks.
- `agents/postmortem`: drafts structured postmortems.
- `agents/memory`: retrieves similar historical incidents and accepts reviewed resolution updates.

## Data Model

- `incident`: id, title, severity, status, started_at, resolved_at.
- `signal`: id, kind, service, timestamp, severity, payload, tags.
- `service`: name, owner, dependencies, criticality.
- `deployment`: service, version, timestamp, author, change_type.
- `hypothesis`: statement, confidence, uncertainty, supporting_signals, contradictory_signals.
- `evidence_link`: source_id, target_id, relationship, weight.
- `action_recommendation`: action_type, target, rationale, risk_level, approval_required.
- `policy_decision`: action_id, level, reason, allowed_without_approval.
- `postmortem`: summary, impact, timeline, root_cause, contributing_factors, follow_ups.
- `memory_case`: incident_id, fingerprint, final_root_cause, services, tags, outcome.

## Workflow

1. Signal Ingestion Agent normalizes scenario signals.
2. Correlation Agent sorts signals, groups anomalies, and creates evidence links.
3. Hypothesis Agent ranks likely causes and tracks uncertainty.
4. Blast Radius Agent walks dependencies to find primary and secondary impact.
5. Policy/Risk Agent gates recommended actions.
6. Action Recommendation Agent emits evidence-backed mitigations.
7. Memory Agent finds similar resolved incidents.
8. Postmortem Agent drafts a reviewable postmortem.
9. Memory updates only after incident review marks the result resolved.

