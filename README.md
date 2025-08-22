[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/gzileni/kgrag-agent-clientt)
[![GitHub stars](https://img.shields.io/github/stars/gzileni/kgrag-agent-client?style=social)](https://github.com/gzileni/kgrag-agent-client/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/gzileni/kgrag-agent-client?style=social)](https://github.com/gzileni/kgrag-agent-client/network)

Client for agent-to-agent (A2A) use, designed for searching and ingesting data into a Neo4j-based knowledge graph. It enables autonomous agents to exchange requests and results (agent-to-agent), enrich and index information via LLMs (e.g., OpenAI, Ollama), and populate the graph with nodes, relationships, and embeddings for semantic search.

## [Docker](./docker/README.md)

## Data ingestion

To ingest a PDF, send a POST request to `http://localhost:8020/chat` with a JSON body containing the `user_input` field set to the file path (for example: `/Users/me/my_file.pdf`):

```bash
curl --location 'http://localhost:8020/chat' \
--header 'Content-Type: application/json' \
--data '{
    "user_input": "/Users/me/my_file.pdf"
}'
```

Note that providing a local file path does not transfer the file contents to the server. To actually ingest the PDF you must either:

- ensure the server has direct access to the given path, or
- upload the file contents (for example via multipart/form-data upload or by including the file encoded in base64 in the JSON).

Also ensure any spaces or special characters in the path are properly quoted/escaped.

## Query

You can use the /chat endpoint to run queries against the knowledge graph. Example curl:

```bash
curl --location --request GET 'http://localhost:8020/chat' \
--header 'Content-Type: application/json' \
--data '{
    "user_input": "Cos'\''è il Machine Learning?"
}'
```

This sends the question to the server and retrieves the response from the knowledge graph.