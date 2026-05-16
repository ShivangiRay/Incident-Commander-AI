from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class SignalKind(str, Enum):
    ALERT = "alert"
    LOG = "log"
    TRACE = "trace"
    METRIC = "metric"
    DEPLOYMENT = "deployment"
    FEATURE_FLAG = "feature_flag"
    RUNBOOK = "runbook"


class RiskLevel(str, Enum):
    SAFE = "safe_to_suggest"
    REVIEW = "requires_human_review"
    NEVER = "never_auto_execute"


class Signal(BaseModel):
    id: str
    kind: SignalKind
    service: str
    timestamp: str
    severity: str = "info"
    message: str
    tags: list[str] = Field(default_factory=list)
    payload: dict = Field(default_factory=dict)


class Incident(BaseModel):
    id: str
    title: str
    severity: str
    status: str
    signals: list[Signal]


class EvidenceLink(BaseModel):
    source_id: str
    target_id: str
    relationship: str
    weight: float


class Timeline(BaseModel):
    incident_id: str
    ordered_signal_ids: list[str]
    evidence_links: list[EvidenceLink]


class Hypothesis(BaseModel):
    id: str
    statement: str
    confidence: float
    uncertainty: str
    supporting_signal_ids: list[str]
    contradictory_signal_ids: list[str] = Field(default_factory=list)


class BlastRadius(BaseModel):
    primary_services: list[str]
    secondary_services: list[str]
    impacted_regions: list[str]
    impacted_endpoints: list[str]


class PolicyDecision(BaseModel):
    action_id: str
    level: RiskLevel
    reason: str
    allowed_without_approval: bool


class ActionRecommendation(BaseModel):
    id: str
    action_type: str
    target: str
    rationale: str
    risk_level: RiskLevel
    approval_required: bool
    supporting_hypothesis_id: str


class MemoryCase(BaseModel):
    incident_id: str
    title: str
    services: list[str]
    tags: list[str]
    final_root_cause: str
    outcome: str

