from pydantic import BaseModel

class Note(BaseModel):
    body: str
