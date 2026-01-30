from pydantic import BaseModel
from typing import Optional

class AIChatResponse(BaseModel):
    answer: str
    model: str