# Incident Commander AI

Multi-agent SRE assistant for incident investigation, evidence correlation, risk-gated action recommendations, memory retrieval, and postmortem drafting.

The bootstrap is deterministic and local-first. It ships with realistic synthetic incident data and generates reasoning artifacts without pretending to connect to live production systems.

## Included

- FastAPI backend in `apps/api`
- React engineering console in `apps/web`
- Agents for ingestion, correlation, hypothesis ranking, blast radius, policy, action recommendation, postmortems, and memory
- Synthetic scenarios for checkout latency, Kafka lag, auth errors, cascading dependency failure, and feature flag rollout
- Policy engine with approval gates
- Evidence timeline, dependency impact graph, and postmortem draft
- Docker Compose for API, web, PostgreSQL, and Redis
- Unit/integration tests

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m libs.common.demo examples/incidents/checkout-latency.json build/incident
uvicorn apps.api.main:app --reload --port 8100
```

Dashboard:

```bash
cd apps/web
npm install
npm run dev
```

Docker:

```bash
docker compose -f infra/docker-compose.yml up --build
```

Demo login:

- Email: `sre@example.com`
- Password: `demo-password`

