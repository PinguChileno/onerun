from pydantic import BaseModel


class RunConversationContext(BaseModel):
    project_id: str
    simulation_id: str
    conversation_id: str
