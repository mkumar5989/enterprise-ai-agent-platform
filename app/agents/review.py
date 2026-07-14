from app.agents.base import Agent

class ReviewAgent(Agent):
    name = "review"
    system_prompt = "Review the proposed solution for security, scalability, reliability, and maintainability."
