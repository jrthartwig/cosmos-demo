# Cosmos DB and Python Azure Functions Project

This project demonstrates how to use Azure Cosmos DB with Python Azure Functions. It includes various endpoints to interact with Cosmos DB, such as retrieving cases and suspects, updating case statuses, and querying suspect profiles by status.


## Endpoints

### 1. Get Case with Suspects

**Route:** `GET /get_case_with_suspects`

**Description:** Retrieves a case and its associated suspects by case ID.

**Parameters:**
- `caseId` (query parameter): The ID of the case to retrieve.

**Example Request:**

```GET /get_case_with_suspects?caseId=FBI12345```


### 2. Get Suspects by Status

**Route:** `GET /get_suspects_by_status`

**Description:** Retrieves suspect profiles by their status.

**Parameters:**
- `status` (query parameter): The status of the suspects to retrieve.

**Example Request:**

```GET /get_suspects_by_status?status=Wanted```


### 3. Update Case Status

**Route:** `PUT /cases/{caseId}/status`

**Description:** Updates the status of a case. If the status is changed to "Closed", the `dateClosed` field is set to the current date.

**Parameters:**
- `caseId` (URL parameter): The ID of the case to update.

**Example Request:**

```
PUT /cases/FBI12345/status
Content-Type: application/json

{
  "status": "Closed"
}
```

**Using Azure Cosmos DB Python SDK**

The Azure Cosmos DB Python SDK provides a set of tools to interact with Cosmos DB. This includes querying documents using SQL-like syntax and updating documents.

**Reading Documents**

To read documents from Cosmos DB, you can use the query_items method. This method allows you to execute SQL-like queries against your Cosmos DB container.

Example: Querying a Document by `caseId`

```python
# Fetch the case document by caseId
query = f"SELECT * FROM c WHERE c.caseId = '{case_id}'"
items = list(case_container.query_items(
    query=query,
    enable_cross_partition_query=True
))
```

**Updating Documents**

To update a document in Cosmos DB, you can use the replace_item method. This method replaces an existing document with a new version.

```python
# Update the case status and dateClosed if status is "Closed"
case_document['status'] = new_status
if new_status.lower() == "closed":
    case_document['dateClosed'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# Replace the document in the container
case_container.replace_item(item=case_document['id'], body=case_document)
```

## Setup

### Prerequisites

- Python 3.6 or later
- Azure Functions Core Tools
- Azure Cosmos DB account
- Visual Studio Code
- Azure Functions VS Code Extension

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-repo/your-project.git
    cd your-project
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create or update `local.settings.json`:**
    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "COSMOS_DB_ENDPOINT": "your-endpoint",
        "COSMOS_DB_KEY": "your-cosmos-db-key",
        "DATABASE_NAME": "your-database-name",
        "CASE_CONTAINER_NAME": "your-case-container-name",
        "SUSPECT_CONTAINER_NAME": "your-suspect-container-name"
      }
    }
    ```

5. **Run the Azure Functions locally:**
    ```sh
    func start
    ```
**References** 
- [Cosmos DB Quick Start](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-portal)
- [Azure Functions with Python Quick Start](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)