import pytest
from app.tools import TOOLS

@pytest.mark.asyncio
async def test_architecture_checklist_tool():
    result = await TOOLS["architecture_checklist"]["handler"]({"stack": ["FastAPI"]})
    assert "authentication" in result["recommended_checks"]
