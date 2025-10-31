from pydantic import BaseModel, Field
from typing import Optional

# Extracted from Document Intelligence
class ContractFields(BaseModel):
    pass

class Message(BaseModel):
    message:str

class Contract(BaseModel):
    record_id:str = Field(alias="recordId")
    data:ContractFields
    errors:Optional[Message]
    warnings:Optional[Message]