import asyncio
import json
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db import init_db, get_session
from app.models import WorkflowRun
from app.schemas import WorkflowRequest, WorkflowResponse
from app.workflow import AgentWorkflow
from app.memory import store_memory, get_memory
from app.tools import TOOLS

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

@app.get(f"{settings.api_v1_prefix}/health")
async def health():
    return {"status": "ok", "service": "enterprise-ai-agent-platform"}

@app.post(f"{settings.api_v1_prefix}/workflows/run", response_model=WorkflowResponse)
async def run_workflow(payload: WorkflowRequest, session: AsyncSession = Depends(get_session)):
    session_id = payload.session_id or str(uuid.uuid4())
    plan, result = await AgentWorkflow().run(payload.objective, payload.context)

    record = WorkflowRun(
        objective=payload.objective,
        context=payload.context,
        plan=plan,
        result=result,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)

    memory_payload = {
        "workflow_id": str(record.id),
        "objective": payload.objective,
        "plan": plan,
        "result": result,
    }
    await store_memory(session_id, memory_payload)

    return WorkflowResponse(
        workflow_id=str(record.id),
        session_id=session_id,
        plan=plan,
        result=result,
    )

@app.post(f"{settings.api_v1_prefix}/workflows/stream")
async def stream_workflow(payload: WorkflowRequest):
    async def generate():
        for stage in ["planner", "research", "coding", "review"]:
            yield f"data: {json.dumps({'stage': stage, 'status': 'started'})}\n\n"
            await asyncio.sleep(0.2)
        plan, result = await AgentWorkflow().run(payload.objective, payload.context)
        yield f"data: {json.dumps({'done': True, 'plan': plan, 'result': result})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get(f"{settings.api_v1_prefix}/memory/{{session_id}}")
async def memory(session_id: str):
    return await get_memory(session_id)

@app.get(f"{settings.api_v1_prefix}/mcp/tools")
async def mcp_tools():
    return {
        "tools": [
            {
                "name": name,
                "description": spec["description"],
                "inputSchema": spec["inputSchema"],
            }
            for name, spec in TOOLS.items()
        ] + [
            {
                "name": "run_workflow",
                "description": "Run the multi-agent workflow.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "objective": {"type": "string"},
                        "context": {"type": "string"},
                    },
                    "required": ["objective"],
                },
            },
            {
                "name": "get_memory",
                "description": "Read workflow memory by session ID.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"session_id": {"type": "string"}},
                    "required": ["session_id"],
                },
            },
        ]
    }

@app.post(f"{settings.api_v1_prefix}/mcp/tools/{{tool_name}}")
async def invoke_tool(tool_name: str, payload: dict):
    if tool_name == "run_workflow":
        plan, result = await AgentWorkflow().run(
            payload.get("objective", ""),
            payload.get("context", ""),
        )
        return {"plan": plan, "result": result}

    if tool_name == "get_memory":
        return await get_memory(payload.get("session_id", ""))

    spec = TOOLS.get(tool_name)
    if not spec:
        raise HTTPException(404, "Tool not found")
    return await spec["handler"](payload)
