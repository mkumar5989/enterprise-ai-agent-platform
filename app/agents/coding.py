from app.agents.base import Agent

class CodingAgent(Agent):
    name = "coding"
    system_prompt = "Propose an implementation structure, modules, APIs, and pseudocode."
