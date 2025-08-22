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

### Description of variables 

- `APP_ENV`  
    Application environment. Typical values: `production`, `development`, `staging`. Affects logging, configuration and runtime behavior.

- `USER_AGENT`  
    Identifier used in HTTP requests (User-Agent). Use a descriptive value to help trace requests.

- `OPENAI_API_KEY`  
    API key for OpenAI (or compatible provider). Secret: do not commit to a public repository. Format: alphanumeric string.

- `AWS_ACCESS_KEY_ID`  
    AWS access key ID for S3 operations. Secret: do not commit. Format: string.

- `AWS_SECRET_ACCESS_KEY`  
    AWS secret access key for S3. Secret: do not commit. Format: string.

- `AWS_REGION`  
    AWS region where the bucket resides (e.g. `eu-central-1`).

- `AWS_BUCKET_NAME`  
    Name of the S3 bucket used for storing data/assets.

- `COLLECTION_NAME`  
    Name of the collection used in Qdrant or another vector DB to store vectors.

- `VECTORDB_SENTENCE_TYPE`  
    Type of embedding model to use for Qdrant: `local` (local model) or `hf` (Hugging Face automatic download). If `local`, also set `VECTORDB_SENTENCE_PATH`; if `hf`, set `VECTORDB_SENTENCE_MODEL`.

- `VECTORDB_SENTENCE_MODEL`  
    Name of the embedding model (e.g. `BAAI/bge-small-en-v1.5` or others listed in the file). For `hf` it will be downloaded from Hugging Face; ignored for `local`.

- `LLM_MODEL_TYPE`  
    Type of LLM provider: supported values in the project e.g. `openai`, `ollama`, `vllm`. Determines the invocation method.

- `LLM_URL`  
    Endpoint of the LLM service (e.g. `http://localhost:11434` for Ollama or a custom API URL).

- `LLM_MODEL_NAME`  
    Name of the LLM model to use on the selected provider (e.g. `tinyllama`, `gpt-4.1-mini`, etc.).

- `MODEL_EMBEDDING`  
    Name of the embedding model for general use (e.g. `nomic-embed-text`, `text-embedding-3-small`). Must be compatible with the chosen provider.

- `NEO4J_USERNAME`  
    Username for connecting to Neo4j.

- `NEO4J_PASSWORD`  
    Password for Neo4j. Secret: do not commit.

- `NEO4J_AUTH`  
    Authentication string for Neo4j, typically in the format `username/password`. Some clients require this combined form.

- `REDIS_URL`  
    Redis connection URL, e.g. `redis://host:port`. May include credentials if needed (be cautious with security).

- `REDIS_HOST`  
    Redis host (used if `REDIS_URL` is not used).

- `REDIS_PORT`  
    Redis port (e.g. `6379`).

- `REDIS_DB`  
    Redis database index to use (integer).

- `APP_VERSION`  
    Application/image version (semver or free-form string) used for tracking/telemetry.

- `A2A_CLIENT`  
    URL of the agent-to-agent (A2A) client used for internal agent communications, e.g. `http://kgrag_agent:8010`.

Security and operational notes:
- Do not place keys and secrets in public repositories. Use a secret manager or an .env file excluded from VCS.  
- Some variables (embedding/LLM models) must be compatible with the local runtime or remote services configured; check the providers' documentation if you encounter loading errors.  
- If you use `VECTORDB_SENTENCE_TYPE=local`, set the local model path via the dedicated variable (not included in the example file).  
- Ensure `NEO4J_AUTH` matches the actual credentials used by the Neo4j container and that the host/container ports in the compose file are correct.  
- For Redis in containerized environments prefer the service host on the overlay network (e.g. `redis://redis:6379`) rather than `localhost`.  
- Change access defaults (e.g. Grafana anonymous admin) before exposing to production.  
- Always rotate keys that have been leaked or accidentally published.

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