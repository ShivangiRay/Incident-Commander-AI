from __future__ import annotations

from libs.common.models import ActionRecommendation, Hypothesis, RiskLevel
from libs.policy.engine import classify_action


class ActionRecommendationAgent:
    name = "action-recommender"

    def recommend(self, hypotheses: list[Hypothesis], severity: str) -> list[ActionRecommendation]:
        actions: list[ActionRecommendation] = []
        for hypothesis in hypotheses[:3]:
            service = hypothesis.id.replace("hyp-", "")
            action_type = "rollback" if hypothesis.confidence >= 0.7 else "page_team"
            level, _ = classify_action(action_type, severity)
            actions.append(
                ActionRecommendation(
                    id=f"act-{service}-{action_type}",
                    action_type=action_type,
                    target=service,
                    rationale=f"{hypothesis.statement} Confidence {hypothesis.confidence:.2f}; start with runbook-matched mitigation.",
                    risk_level=level,
                    approval_required=level != RiskLevel.SAFE,
                    supporting_hypothesis_id=hypothesis.id,
                )
            )
        return actions

