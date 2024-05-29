
from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    model_config = ConfigDict(extra='allow')
    title: str
    source: str
    url: str
    description: str = None
    
