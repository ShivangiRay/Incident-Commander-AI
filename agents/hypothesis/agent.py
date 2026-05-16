from __future__ import annotations

from libs.common.models import Hypothesis, Incident, Timeline


class HypothesisAgent:
    name = "hypothesis"

    def rank(self, incident: Incident, timeline: Timeline) -> list[Hypothesis]:
        deploy_services = {signal.service for signal in incident.signals if signal.kind.value == "deployment"}
        alert_services = {signal.service for signal in incident.signals if signal.kind.value == "alert"}
        hypotheses: list[Hypothesis] = []
        for service in sorted(deploy_services | alert_services):
            supporting = [
                signal.id
                for signal in incident.signals
                if signal.service == service or service in signal.tags or any(link.source_id == signal.id for link in timeline.evidence_links)
            ]
            confidence = min(0.95, 0.45 + len(supporting) * 0.12)
            hypotheses.append(
                Hypothesis(
                    id=f"hyp-{service}",
                    statement=f"Recent change or dependency degradation in {service} is driving the incident.",
                    confidence=round(confidence, 2),
                    uncertainty="medium" if confidence < 0.75 else "low",
                    supporting_signal_ids=supporting,
                    contradictory_signal_ids=[],
                )
            )
        return sorted(hypotheses, key=lambda item: item.confidence, reverse=True)

