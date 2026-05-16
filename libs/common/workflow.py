from __future__ import annotations

import json
import shutil
from pathlib import Path

from agents.action_recommender.agent import ActionRecommendationAgent
from agents.blast_radius.agent import BlastRadiusAgent
from agents.correlation.agent import CorrelationAgent
from agents.hypothesis.agent import HypothesisAgent
from agents.ingestion.agent import SignalIngestionAgent
from agents.memory.agent import LearningMemoryAgent
from agents.policy.agent import PolicyRiskAgent
from agents.postmortem.agent import PostmortemAgent


class IncidentWorkflow:
    def run(self, scenario_path: str | Path, output_dir: str | Path) -> dict:
        root = Path(output_dir)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)

        incident = SignalIngestionAgent().ingest(scenario_path)
        timeline = CorrelationAgent().correlate(incident)
        hypotheses = HypothesisAgent().rank(incident, timeline)
        blast = BlastRadiusAgent().estimate(incident)
        actions = ActionRecommendationAgent().recommend(hypotheses, incident.severity)
        policy_decisions = [PolicyRiskAgent().decide(action, incident.severity) for action in actions]
        similar = LearningMemoryAgent().similar(incident)
        postmortem = PostmortemAgent().draft(incident, timeline, hypotheses, blast, actions)

        (root / "incident.json").write_text(incident.model_dump_json(indent=2))
        (root / "timeline.json").write_text(timeline.model_dump_json(indent=2))
        (root / "hypotheses.json").write_text(json.dumps([item.model_dump() for item in hypotheses], indent=2))
        (root / "blast-radius.json").write_text(blast.model_dump_json(indent=2))
        (root / "actions.json").write_text(json.dumps([item.model_dump() for item in actions], indent=2))
        (root / "policy-decisions.json").write_text(json.dumps([item.model_dump() for item in policy_decisions], indent=2))
        (root / "similar-incidents.json").write_text(json.dumps([item.model_dump() for item in similar], indent=2))
        (root / "postmortem-draft.md").write_text(postmortem)
        return {
            "incident": incident,
            "timeline": timeline,
            "hypotheses": hypotheses,
            "blast": blast,
            "actions": actions,
            "policy_decisions": policy_decisions,
            "similar": similar,
            "postmortem": postmortem,
        }

