from pydantic import BaseModel, Field, ConfigDict
from typing import List

class BlobMetadata(BaseModel):
    #model_config = ConfigDict(populate_by_name=True)
    metadata_storage_name: str

class DocumentInformation(BaseModel):
    #model_config = ConfigDict(populate_by_name=True)
    recordId: str
    blob_metadata_data: BlobMetadata = Field(alias="data")

class DocumentRequest(BaseModel):
    values: List[DocumentInformation]