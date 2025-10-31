from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
import os

class ContractService:
    def __init__(self):
        self.doc_client = DocumentIntelligenceClient(
            endpoint=os.getenv('DOC_ENDPOINT'),
            credential=AzureKeyCredential(os.getenv('DOC_API_KEY'))
        )
        self.account_name = os.getenv('BLOB_ACCOUNT_NAME')
        self.container_name = os.getenv('CONTAINER_NAME')

    async def analyze_contract(self,file_name:str):

        blob = BlobClient(
            account_url=self.account_name,
            container_name=self.container_name,
            credential=DefaultAzureCredential()
        )

        poller = await self.doc_client.begin_analyze_document(
            model_id="prebuilt-contract",
            body=AnalyzeDocumentRequest(url_source=blob.url)
            #query_fields=[]  # Todo
        )

        contract_extraction = await poller.result()