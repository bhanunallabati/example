import logging
import pyodbc
import json
import azure.functions as func
from azure.identity import ManagedIdentityCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get database connection details from environment variables or hardcode them
    server = "your_sql_server.database.windows.net"
    database = "your_database_name"
    
    # Set up the Managed Identity credential
    managed_identity_credential = ManagedIdentityCredential(client_id="your-user-assigned-client-id")

    # Build the connection string
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database}'

    try:
        # Authenticate and get the token for SQL authentication
        token = managed_identity_credential.get_token("https://database.windows.net/.default")
        
        # Create a connection using the managed identity token
        conn = pyodbc.connect(conn_str, attrs_before={1256: token.token})

        cursor = conn.cursor()

        # Example SQL query to execute
        sql_query = "SELECT TOP 10 * FROM your_table"
        cursor.execute(sql_query)

        # Fetch the results
        rows = cursor.fetchall()

        # Create a JSON response
        result = []
        for row in rows:
            result.append({desc[0]: value for desc, value in zip(cursor.description, row)})

        # Close the connection
        cursor.close()
        conn.close()

        # Return the result as a JSON response
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Log the error
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            f"Error executing SQL query: {str(e)}",
            status_code=500
        )
