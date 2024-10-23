from function_app import app, suspect_container
import azure.functions as func
import logging

@app.route(route="get_suspects_by_status")
def get_suspects_by_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to get suspects by status.')

    status = req.params.get('status')
    if not status:
        return func.HttpResponse(
            "Please pass a status in the query string.",
            status_code=400
        )

    try:
        # Query the suspect documents by status
        query = f"SELECT * FROM c WHERE c.status = '{status}'"
        items = list(suspect_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if not items:
            logging.error(f"No suspects with status {status} found.")
            return func.HttpResponse(
                "No suspects found.",
                status_code=404
            )

        logging.info(f"Suspect documents retrieved: {items}")

        return func.HttpResponse(
            body=str(items),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            "An error occurred while fetching the suspects.",
            status_code=500
        )