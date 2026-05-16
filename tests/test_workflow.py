from pathlib import Path

from libs.common.workflow import IncidentWorkflow
from libs.policy.engine import classify_action


SCENARIO = Path("examples/incidents/checkout-latency.json")


def test_policy_requires_review_for_rollback() -> None:
    level, reason = classify_action("rollback", "sev1")
    assert level.value == "requires_human_review"
    assert "review" in reason.lower()


def test_full_incident_workflow_generates_artifacts(tmp_path: Path) -> None:
    result = IncidentWorkflow().run(SCENARIO, tmp_path)
    assert result["hypotheses"][0].confidence >= 0.6
    assert result["policy_decisions"][0].allowed_without_approval is False
    assert (tmp_path / "timeline.json").exists()
    assert (tmp_path / "postmortem-draft.md").exists()
    assert "Postmortem Draft" in (tmp_path / "postmortem-draft.md").read_text()

