from typing import List, Optional
from pydantic import BaseModel, field_validator

class ErrorExplanation(BaseModel):
    original: str
    corrected: str
    explanation: str

class ChatTurn(BaseModel):
    user_input: str
    corrected: Optional[str] = None
    errors: Optional[List[ErrorExplanation]] = None
    grade: Optional[str] = None
    agent_response: Optional[str] = None

    field_validator('grade')
    @classmethod
    def validate_grade(cls, v):
        if v and v not in ['green', 'orange', 'red']:
            raise ValueError("grade must be one of: green, orange, red")
        return v
    
class AgentState(BaseModel):
    history: List[ChatTurn] = []
