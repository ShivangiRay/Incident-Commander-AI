from __future__ import annotations

from libs.common.models import EvidenceLink, Incident, Timeline


class CorrelationAgent:
    name = "correlation"

    def correlate(self, incident: Incident) -> Timeline:
        ordered = sorted(incident.signals, key=lambda item: item.timestamp)
        links: list[EvidenceLink] = []
        deploys = [signal for signal in ordered if signal.kind.value == "deployment"]
        for signal in ordered:
            if signal.kind.value in {"alert", "metric", "trace", "log"}:
                for deploy in deploys:
                    if deploy.service == signal.service or deploy.service in signal.tags:
                        links.append(
                            EvidenceLink(
                                source_id=deploy.id,
                                target_id=signal.id,
                                relationship="temporally_correlated_with",
                                weight=0.82,
                            )
                        )
        return Timeline(incident_id=incident.id, ordered_signal_ids=[signal.id for signal in ordered], evidence_links=links)

