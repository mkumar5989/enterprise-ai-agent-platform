from app.llm import get_llm

class Agent:
    name = "agent"
    system_prompt = "You are a helpful enterprise software agent."

    async def run(self, objective: str, context: str, shared: dict) -> dict:
        prompt = f"Objective: {objective}\nContext: {context}\nShared: {shared}"
        output = await get_llm().complete(self.system_prompt, prompt)
        return {"agent": self.name, "output": output}
