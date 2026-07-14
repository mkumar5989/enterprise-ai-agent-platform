from app.agents.base import Agent

class ResearchAgent(Agent):
    name = "research"
    system_prompt = "Analyze the objective and identify risks, assumptions, and technical considerations."
