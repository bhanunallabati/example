import logging
import pyodbc
import json
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get database connection details from environment variables or hardcode them
    server = os.getenv('SQL_SERVER', 'your_sql_server.database.windows.net')
    database = os.getenv('SQL_DATABASE', 'your_database_name')
    username = os.getenv('SQL_USERNAME', 'your_sql_username')
    password = os.getenv('SQL_PASSWORD', 'your_sql_password')

    # Build the connection string for SQL authentication
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        # Create a connection using the SQL Server username and password
        conn = pyodbc.connect(conn_str)

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
