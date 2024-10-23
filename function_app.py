import azure.functions as func
import logging
from azure.cosmos import CosmosClient
import os

# Initialize the Cosmos client
endpoint = os.getenv("COSMOS_DB_ENDPOINT")
key = os.getenv("COSMOS_DB_KEY")
client = CosmosClient(endpoint, key)
database_name = os.getenv("DATABASE_NAME")
case_container_name = os.getenv("CASE_CONTAINER_NAME")
suspect_container_name = os.getenv("SUSPECT_CONTAINER_NAME")
database = client.get_database_client(database_name)
case_container = database.get_container_client(case_container_name)
suspect_container = database.get_container_client(suspect_container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_case_with_suspects")
def get_case_with_suspects(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to get case and suspects by case ID.')

    case_id = req.params.get('caseId')
    if not case_id:
        return func.HttpResponse(
            "Please pass a caseId in the query string.",
            status_code=400
        )

    try:
        # Query the case document by caseId
        query = f"SELECT * FROM c WHERE c.caseId = '{case_id}'"
        items = list(case_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if not items:
            logging.error(f"Case with ID {case_id} not found.")
            return func.HttpResponse(
                "Case not found.",
                status_code=404
            )

        case_document = items[0]
        logging.info(f"Case document retrieved: {case_document}")

        # Fetch the suspect documents
        suspect_documents = []
        for suspect_id in case_document.get('suspectIds', []):
            try:
                logging.info(f"Fetching suspect with ID: {suspect_id}")
                query = f"SELECT * FROM c WHERE c.suspectId = '{suspect_id}'"
                items = list(suspect_container.query_items(
                    query=query,
                    enable_cross_partition_query=True
                ))

                if items:
                    suspect_document = items[0]
                    suspect_documents.append(suspect_document)
                    logging.info(f"Suspect document retrieved: {suspect_document}")
                else:
                    logging.warning(f"Suspect with ID {suspect_id} not found.")
            except Exception as e:
                logging.error(f"An error occurred while fetching suspect with ID {suspect_id}: {e}")
        
        # Combine case and suspects into one response
        response = {
            "case": case_document,
            "suspects": suspect_documents
        }

        return func.HttpResponse(
            body=str(response),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            "An error occurred while fetching the case and suspects.",
            status_code=500
        )