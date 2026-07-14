from pydantic import BaseModel, Field

class WorkflowRequest(BaseModel):
    objective: str = Field(min_length=5, max_length=4000)
    context: str = Field(default="", max_length=8000)
    session_id: str | None = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    session_id: str
    plan: dict
    result: dict
