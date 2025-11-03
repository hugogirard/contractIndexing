from pydantic import BaseModel, Field
from typing import Optional, List

class Jurisdiction(BaseModel):
    region:Optional[str] = None
    clause:Optional[str] = None

class Party(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    reference_name: Optional[str] = Field(default=None, alias="referenceName")
    clause: Optional[str] = None

# Extracted from Document Intelligence
class ContractFields(BaseModel):
    doc_type:Optional[str] = Field(default=None,alias="docType")
    title:Optional[str] = None
    contract_id: Optional[str] = Field(default=None, alias="contractId")
    parties:List[Party] = []
    execution_date: Optional[str] = Field(default=None, alias="executionDate")
    effective_date:Optional[str] = Field(default=None,alias="effectiveDate")
    expiration_date: Optional[str] = Field(default=None, alias="expirationDate")
    contract_duration: Optional[str] = Field(default=None, alias="contractDuration")
    renewal_date: Optional[str] = Field(default=None, alias="renewalDate")
    jurisdictions:List[str] = []

class Message(BaseModel):
    message:str

class Contract(BaseModel):
    record_id:str = Field(default=None, alias="recordId")
    data:ContractFields
    errors:Optional[Message] = None
    warnings:Optional[Message] = None