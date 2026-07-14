from datetime import datetime

async def current_time_tool(_: dict) -> dict:
    return {"utc": datetime.utcnow().isoformat() + "Z"}

async def architecture_checklist_tool(payload: dict) -> dict:
    stack = payload.get("stack", [])
    checks = [
        "authentication",
        "authorization",
        "observability",
        "rate limiting",
        "data validation",
        "caching",
        "deployment strategy",
        "backup strategy",
    ]
    return {"stack": stack, "recommended_checks": checks}

TOOLS = {
    "current_time": {
        "description": "Return current UTC time.",
        "handler": current_time_tool,
        "inputSchema": {"type": "object", "properties": {}},
    },
    "architecture_checklist": {
        "description": "Return an enterprise architecture checklist.",
        "handler": architecture_checklist_tool,
        "inputSchema": {
            "type": "object",
            "properties": {"stack": {"type": "array", "items": {"type": "string"}}},
        },
    },
}
