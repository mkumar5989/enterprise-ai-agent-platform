from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.coding import CodingAgent
from app.agents.review import ReviewAgent

class AgentWorkflow:
    def __init__(self):
        self.planner = PlannerAgent()
        self.research = ResearchAgent()
        self.coding = CodingAgent()
        self.review = ReviewAgent()

    async def run(self, objective: str, context: str) -> tuple[dict, dict]:
        shared: dict = {}
        plan = await self.planner.run(objective, context, shared)
        shared["plan"] = plan

        research = await self.research.run(objective, context, shared)
        shared["research"] = research

        coding = await self.coding.run(objective, context, shared)
        shared["coding"] = coding

        review = await self.review.run(objective, context, shared)
        shared["review"] = review

        return plan, {
            "research": research,
            "coding": coding,
            "review": review,
        }
