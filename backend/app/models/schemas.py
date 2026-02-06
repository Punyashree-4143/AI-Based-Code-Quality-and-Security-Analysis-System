from pydantic import BaseModel
from typing import Optional, Dict

class ReviewRequest(BaseModel):
    language: str
    context: str
    code: str
    metadata: Optional[Dict] = None
