from pydantic import BaseModel
from typing import Optional

class FeedbackRequest(BaseModel):
    feedback_text: str
    user_id: Optional[str] = "anonymous"
