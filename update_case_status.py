from function_app import app, case_container
import azure.functions as func
import logging
from datetime import datetime, timezone

@app.route(route="cases/{caseId}/status", methods=["PUT"])
def update_case_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to update case status.')

    case_id = req.route_params.get('caseId')
    if not case_id:
        return func.HttpResponse(
            "Please provide a caseId in the URL.",
            status_code=400
        )

    try:
        # Parse the request body
        req_body = req.get_json()
        new_status = req_body.get('status')

        if not new_status:
            return func.HttpResponse(
                "Please provide a status in the request body.",
                status_code=400
            )

        # Fetch the case document by caseId
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

        # Update the case status and dateClosed if status is "Closed"
        case_document['status'] = new_status
        if new_status.lower() == "closed":
            case_document['dateClosed'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        # Replace the document in the container
        case_container.replace_item(item=case_document['id'], body=case_document)
        logging.info(f"Case document updated: {case_document}")

        return func.HttpResponse(
            body=str(case_document),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            "An error occurred while updating the case status.",
            status_code=500
        )