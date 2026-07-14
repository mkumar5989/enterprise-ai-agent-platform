from app.agents.base import Agent

class PlannerAgent(Agent):
    name = "planner"
    system_prompt = "Create a concise step-by-step implementation plan."

    async def run(self, objective: str, context: str, shared: dict) -> dict:
        result = await super().run(objective, context, shared)
        result["steps"] = [
            "Clarify scope and constraints",
            "Define architecture",
            "Identify data and integration needs",
            "Implement core workflow",
            "Add testing and deployment",
        ]
        return result
