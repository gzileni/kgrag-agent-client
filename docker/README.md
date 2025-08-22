# Docker

A collection of Docker Compose services to run the kgrag stack:
- kgrag-mcp-server (MCP backend + Redis, Qdrant, Neo4j)
- kgrag-agent (agent connecting to MCP via SSE)
- kgrag-loki (log aggregator)
- kgrag-promtail (log forwarder)
- kgrag-grafana (log/metrics visualization)

## Requirements
- Docker & Docker Compose (or Docker CLI with `docker compose` support)  
- A `.env` file containing the environment variables listed below

## Services and key points

### kgrag-mcp-server
- Image: `ghcr.io/gzileni/kgrag_mcp_server:main`
- Ports:
    - `8000:8000` — HTTP MCP
    - `6379:6379` — Redis
    - `6333:6333`, `6334:6334` — Qdrant
    - `7474:7474` — Neo4j HTTP
    - `7687:7687` — Neo4j Bolt
- Persistent volumes: `qdrant_data`, `redis_data`, `neo4j_data`
- Environment: multiple variables for LLM, AWS, Neo4j, Loki, etc.
- Profiles: `mcp`, `all`
- Network: `kgrag-network`

### kgrag-agent
- Image: `ghcr.io/gzileni/kgrag-agent:main`
- Port: `8010:8010` (also exposed internally)
- Connects to MCP via SSE: `MCP_SERVER_KGRAG=http://kgrag_mcp_server:8000/sse`
- Depends on Redis and Qdrant provided by the MCP server via the network
- Profiles: `agent`, `all`

### kgrag-loki
- Image: `grafana/loki:latest`
- Port: `3100:3100`
- Used as the log push endpoint (`LOKI_URL`)

### kgrag-promtail
- Image: `grafana/promtail:latest`
- Volume: `loki_log:/var/log`
- Local log forwarder to Loki

### kgrag-grafana
- Image: `grafana/grafana:latest`
- Port: `3000:3000`
- Auto-provisions a Loki datasource (anonymous access enabled)
- Volume: `grafana_data:/var/lib/grafana`

## Network and volumes
- Network: `kgrag-network` (bridge) — subnet configured as `172.16.110.0/24`  
- Persistent volumes:
    - `qdrant_data`
    - `redis_data`
    - `neo4j_data`
    - `grafana_data`
    - `loki_log`

## Required environment variables (example minimal `.env`)
- APP_ENV
- LLM_MODEL_TYPE
- OPENAI_API_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_BUCKET_NAME
- COLLECTION_NAME
- LLM_MODEL_NAME
- MODEL_EMBEDDING
- LLM_URL
- NEO4J_USERNAME
- NEO4J_PASSWORD
- NEO4J_AUTH
- USER_AGENT

## Usage examples
- Start all services (profile `all`):
    - `docker compose --profile all up -d`
- Start only MCP and dependencies:
    - `docker compose --profile mcp up -d`
- Start only agent:
    - `docker compose --profile agent up -d`
- Stop and remove (including volumes):
    - docker compose down --volumes

## Makefile — available options

- **dev** — start the stack with the "dev" profile
- **stop-dev** — stop the "dev" profile stack
- **mcp** — start the MCP backend and its dependencies (profile "mcp")
- **stop-mcp** — stop the MCP profile stack
- **agent** — start the agent service (profile "agent")
- **stop-agent** — stop the agent profile stack
- **run** — start all services (profile "all")
- **stop** — stop all services (profile "all")
- **restart** — stop and then start all services

Quick usage:
- `make dev` / `make stop-dev`
- `make mcp` / `make stop-mcp`
- `make agent` / `make stop-agent`
- `make run` / `make stop` / `make restart`

## Operational notes and recommendations
- Place the `.env` file in the same folder as the docker-compose file or export variables in the environment.
- Services communicate via the `kgrag-network`; you do not need to expose all ports publicly in production.
- Grafana is configured for anonymous Admin access — change this for production.
- Verify volumes for data persistence (Qdrant, Redis, Neo4j, Grafana).
- For debugging: `docker compose logs -f <service_name>`

## Contacts and resources
- Images are hosted on GitHub Container Registry / Docker Hub (tags used: `:main` / `:latest`).  
- Change images/tags according to the desired release channels.

-----------------------------------------------------------------------------
File: docker/README.md — generated automatically.