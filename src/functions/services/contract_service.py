from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzedDocument, AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
from models import Jurisdiction, ContractFields
from typing import List
import os
import logging

class ContractService:
    def __init__(self):
        self.doc_client = DocumentIntelligenceClient(
            endpoint=os.getenv('DOC_ENDPOINT'),
            credential=AzureKeyCredential(os.getenv('DOC_API_KEY'))
        )
        self.account_name = os.getenv('BLOB_ACCOUNT_URL')
        self.container_name = os.getenv('CONTAINER_NAME')

    async def analyze_contract(self,file_name:str) -> ContractFields:

        try:
            
            blob = BlobClient(
                account_url=self.account_name,
                container_name=self.container_name,
                blob_name=file_name,
                credential=DefaultAzureCredential()
            )

            poller = await self.doc_client.begin_analyze_document(
                model_id="prebuilt-contract",
                body=AnalyzeDocumentRequest(url_source=blob.url)
                #query_fields=[]  # Todo
            )

            contract = await poller.result()

            doc = contract.documents[0]

            return self._extract_schema_document(doc)
                      
        except Exception as ex:
            raise logging.error(ex)
    
    def _extract_schema_document(self,doc:AnalyzedDocument) -> ContractFields:

        contract_fields:ContractFields = ContractFields()

        if doc.doc_type:
            contract_fields.doc_type = doc.doc_type

        title = doc.fields.get("Title")
        if title:
            contract_fields.title = title.value_string

        effective_date = doc.fields.get("EffectiveDate")
        if effective_date:
            contract_fields.effective_date = effective_date.value_string

        parties = doc.fields.get("Parties")
        if parties:
            contract_parties:List[str] = []
            for party_idx, party in enumerate(parties.value_array):
                contract_parties.append(party.value_string)
            contract_fields.parties = contract_parties

        jurisdictions = doc.fields.get("Jurisdictions")
        if jurisdictions:
            contract_jurisdictions:List[Jurisdiction] = []
            for jurisdiction_idx, jurisdiction in enumerate(jurisdictions.value_array):
                
                contract_jurisdiction = Jurisdiction()
                
                region = jurisdiction.value_object.get("Region")
                if region:
                    contract_jurisdiction.region = region.value_string

                clause = jurisdiction.value_object.get("Clause")
                if clause:
                    contract_jurisdiction.clause = clause.value_string
                
                contract_jurisdictions.append(contract_jurisdiction)
            
            contract_fields.jurisdictions = contract_jurisdictions

        return contract_fields

