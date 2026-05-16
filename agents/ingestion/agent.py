from __future__ import annotations

import json
from pathlib import Path

from libs.common.models import Incident, Signal


class SignalIngestionAgent:
    name = "ingestion"

    def ingest(self, path: str | Path) -> Incident:
        raw = json.loads(Path(path).read_text())
        return Incident(
            id=raw["id"],
            title=raw["title"],
            severity=raw["severity"],
            status=raw.get("status", "active"),
            signals=[Signal(**signal) for signal in raw["signals"]],
        )

