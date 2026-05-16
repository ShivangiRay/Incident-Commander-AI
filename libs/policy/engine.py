from __future__ import annotations

from libs.common.models import RiskLevel


NEVER_ACTIONS = {"delete_data", "drop_database", "purge_queue"}
REVIEW_ACTIONS = {"rollback", "traffic_shift", "scale_up", "disable_feature_flag", "circuit_break"}


def classify_action(action_type: str, severity: str) -> tuple[RiskLevel, str]:
    if action_type in NEVER_ACTIONS:
        return RiskLevel.NEVER, "Destructive operations are never auto-executed."
    if action_type in REVIEW_ACTIONS or severity in {"sev1", "critical"}:
        return RiskLevel.REVIEW, "Operational change requires human review for this severity/action class."
    return RiskLevel.SAFE, "Read-only or low-risk recommendation."

