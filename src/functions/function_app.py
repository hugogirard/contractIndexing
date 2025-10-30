from azure.functions import HttpMethod
from request import DocumentRequest
from pydantic import ValidationError
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="process_contract")
@app.route(route="process",methods=[HttpMethod.POST])
def process_contract(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    try:
        req_body = req.get_json()
        document_request = DocumentRequest(**req_body)
        
    except ValueError as ex:
        logging.error(ex)
        return func.HttpResponse("The payload body is null", status_code=400)
    except ValidationError as e:
        return func.HttpResponse(f"Invalid request format: {str(e)}", status_code=400)

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )