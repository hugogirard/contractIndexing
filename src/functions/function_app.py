from azure.functions import HttpMethod
from request import DocumentRequest, DocumentOutput
from pydantic import ValidationError
from services.contract_service import ContractService
from models import ContractFields, Contract, Message
import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

contract_service = ContractService()

@app.route(route="process", methods=[HttpMethod.POST])
async def process_contract(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    try:
        req_body = req.get_json()
        document_request = DocumentRequest(**req_body)
        document_output = DocumentOutput(values=[])

        for doc in document_request.values:

            try:
                contract_fields:ContractFields = await contract_service.analyze_contract(file_name=doc.blob_metadata_data.metadata_storage_name)
                
                contract = Contract(
                    recordId=doc.recordId,
                    data=contract_fields
                )
                
                document_output.values.append(contract)
            except Exception as ex:
                # Keeping the document in errors
                contract = Contract(
                    recordId=doc.recordId,
                    data=ContractFields(),
                    errors=Message(
                        message=str(ex)
                    )
                )
                document_output.values.append(contract)


            
        return func.HttpResponse(document_output.model_dump_json(indent=4, by_alias=True),
                                 mimetype="application/json",
                                 status_code=200)

    except ValueError as ex:
        logging.error(ex)
        return func.HttpResponse("The payload body is null", status_code=400)
    except ValidationError as e:
        return func.HttpResponse(f"Invalid request format: {str(e)}", status_code=400)