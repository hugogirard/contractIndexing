from pydantic import BaseModel, Field
from typing import Optional, List

class Jurisdiction(BaseModel):
    region:Optional[str]
    clause:Optional[str]

# Extracted from Document Intelligence
class ContractFields(BaseModel):
    doc_type:Optional[str] = Field(default=None,alias="docType")
    title:Optional[str] = None
    effective_date:Optional[str] = Field(default=None,alias="effectiveDate")
    parties:List[str] = []
    jurisdictions:List[str] = []

class Message(BaseModel):
    message:str

class Contract(BaseModel):
    record_id:str = Field(default=None, alias="recordId")
    data:ContractFields
    errors:Optional[Message] = None
    warnings:Optional[Message] = None