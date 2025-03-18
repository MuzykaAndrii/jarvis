from pydantic import BaseModel


class LLMOutputSchema(BaseModel):
    text: str
