from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from libs.common.workflow import IncidentWorkflow


app = FastAPI(title="Incident Commander AI")


class InvestigateRequest(BaseModel):
    scenario_path: str
    output_dir: str = "build/incident"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/incidents/investigate")
def investigate(request: InvestigateRequest) -> dict:
    scenario = Path(request.scenario_path)
    if not scenario.exists():
        raise HTTPException(status_code=404, detail="Scenario file not found")
    result = IncidentWorkflow().run(scenario, request.output_dir)
    return {
        "incidentId": result["incident"].id,
        "topHypothesis": result["hypotheses"][0].statement,
        "recommendedActions": len(result["actions"]),
        "approvalRequired": sum(1 for action in result["actions"] if action.approval_required),
        "postmortemPath": str(Path(request.output_dir) / "postmortem-draft.md"),
    }

