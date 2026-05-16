from __future__ import annotations

from libs.common.models import ActionRecommendation, BlastRadius, Hypothesis, Incident, Timeline


class PostmortemAgent:
    name = "postmortem"

    def draft(self, incident: Incident, timeline: Timeline, hypotheses: list[Hypothesis], blast: BlastRadius, actions: list[ActionRecommendation]) -> str:
        top = hypotheses[0]
        lines = [
            f"# Postmortem Draft: {incident.title}",
            "",
            "## Summary",
            f"{incident.severity.upper()} incident with strongest current hypothesis: {top.statement}",
            "",
            "## Impact",
            f"Primary services: {', '.join(blast.primary_services)}. Secondary services: {', '.join(blast.secondary_services) or 'none detected'}.",
            "",
            "## Timeline",
        ]
        for signal_id in timeline.ordered_signal_ids:
            signal = next(item for item in incident.signals if item.id == signal_id)
            lines.append(f"- {signal.timestamp} `{signal.kind.value}` `{signal.service}`: {signal.message}")
        lines.extend(["", "## Root Cause", top.statement, "", "## Recommended Actions"])
        for action in actions:
            lines.append(f"- `{action.action_type}` `{action.target}`: {action.rationale} Risk: {action.risk_level.value}.")
        lines.extend(["", "## Follow-up Items", "- Review owner feedback before updating incident memory."])
        return "\n".join(lines)

