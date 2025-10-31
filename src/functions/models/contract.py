from pydantic import BaseModel, Field
from typing import Optional, List

class Jurisdiction(BaseModel):
    region:Optional[str]
    clause:Optional[str]

# Extracted from Document Intelligence
class ContractFields(BaseModel):
    doc_type:Optional[str] = Field(alias="docType")
    title:Optional[str]
    effective_date:Optional[str] = Field(alias="effectiveDate")
    parties:List[str]
    jurisdictions:List[str]

class Message(BaseModel):
    message:str

class Contract(BaseModel):
    record_id:str = Field(alias="recordId")
    data:ContractFields
    errors:Optional[Message]
    warnings:Optional[Message]