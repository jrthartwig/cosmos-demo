import azure.functions as func
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

import get_case_with_suspects