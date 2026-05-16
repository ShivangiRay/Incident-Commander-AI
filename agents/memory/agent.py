from __future__ import annotations

from libs.common.models import Incident, MemoryCase


MEMORY = [
    MemoryCase(
        incident_id="mem-001",
        title="Checkout latency after payments deploy",
        services=["checkout", "payments"],
        tags=["latency", "deployment", "/checkout"],
        final_root_cause="Payments client timeout regression after deploy.",
        outcome="Rolled back payments v2026.05.10 and latency recovered.",
    )
]


class LearningMemoryAgent:
    name = "memory"

    def similar(self, incident: Incident) -> list[MemoryCase]:
        services = {signal.service for signal in incident.signals}
        tags = {tag for signal in incident.signals for tag in signal.tags}
        scored = []
        for case in MEMORY:
            score = len(services & set(case.services)) + len(tags & set(case.tags))
            if score:
                scored.append((score, case))
        return [case for _, case in sorted(scored, key=lambda item: item[0], reverse=True)]

