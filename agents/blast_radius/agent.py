from __future__ import annotations

from libs.common.models import BlastRadius, Incident


DEPENDENCIES = {
    "checkout": ["payments", "inventory", "orders"],
    "payments": ["billing"],
    "auth": ["user-profile"],
    "notifications": ["email-provider"],
    "orders": ["kafka-orders"],
}


class BlastRadiusAgent:
    name = "blast-radius"

    def estimate(self, incident: Incident) -> BlastRadius:
        primary = sorted({signal.service for signal in incident.signals if signal.severity in {"critical", "warning"}})
        secondary = sorted({dep for service in primary for dep in DEPENDENCIES.get(service, [])})
        regions = sorted({signal.payload.get("region", "global") for signal in incident.signals})
        endpoints = sorted({tag for signal in incident.signals for tag in signal.tags if tag.startswith("/")})
        return BlastRadius(primary_services=primary, secondary_services=secondary, impacted_regions=regions, impacted_endpoints=endpoints)

