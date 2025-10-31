from pydantic import BaseModel
from models import Contract
from typing import List

class DocumentOutput(BaseModel):
    values: List[Contract]