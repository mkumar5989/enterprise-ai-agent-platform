import pytest
from app.workflow import AgentWorkflow

@pytest.mark.asyncio
async def test_workflow_local_mode():
    plan, result = await AgentWorkflow().run(
        "Design a scalable API",
        "Use FastAPI and PostgreSQL"
    )
    assert plan["agent"] == "planner"
    assert "research" in result
    assert "coding" in result
    assert "review" in result
