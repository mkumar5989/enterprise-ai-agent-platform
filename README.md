# Enterprise AI Agent Platform

A portfolio-ready multi-agent orchestration API built with FastAPI.

## Features

- Planner, Research, Coding, and Review agents
- Deterministic local demo mode
- Optional OpenAI provider
- Tool registry
- MCP-style tool manifest and invocation endpoints
- Redis-backed short-term memory
- PostgreSQL-backed workflow history
- Directed agent workflow
- Streaming responses
- Docker Compose
- Swagger/OpenAPI
- Unit tests
- GitHub Actions CI

## Architecture

```text
Client
  |
  v
FastAPI
  |
  v
Planner Agent
  |
  +--> Research Agent
  +--> Coding Agent
  +--> Review Agent
  |
  v
Workflow Result
  |
  +--> PostgreSQL history
  +--> Redis memory
  +--> MCP-style tools
```

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Demo Request

```bash
curl -X POST http://localhost:8000/api/v1/workflows/run \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Design a scalable invoice-processing API",
    "context": "Use FastAPI, PostgreSQL and Redis"
  }'
```

## Provider Modes

Local mode works without an API key:

```env
LLM_PROVIDER=local
```

OpenAI mode:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

## MCP-Style Endpoints

- `GET /api/v1/mcp/tools`
- `POST /api/v1/mcp/tools/run_workflow`
- `POST /api/v1/mcp/tools/get_memory`

These endpoints expose platform capabilities as tool-like operations and can be adapted to a full MCP transport.

## Notes

This repository is a portfolio-grade starter, not a drop-in production system. Before public production use, add:
- authentication and authorization
- tenant isolation
- observability
- durable queues
- secrets management
- migrations
- policy controls
- human approval checkpoints

## License

MIT
