from __future__ import annotations

from libs.common.models import ActionRecommendation, PolicyDecision
from libs.policy.engine import classify_action


class PolicyRiskAgent:
    name = "policy"

    def decide(self, recommendation: ActionRecommendation, severity: str) -> PolicyDecision:
        level, reason = classify_action(recommendation.action_type, severity)
        return PolicyDecision(
            action_id=recommendation.id,
            level=level,
            reason=reason,
            allowed_without_approval=level.value == "safe_to_suggest",
        )

