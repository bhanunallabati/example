import pyodbc
import msal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Azure AD and SQL Server details
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
SQL_SERVER = "your-sql-server.database.windows.net"
DATABASE_NAME = "your-database-name"

# Get an access token from Azure AD
def get_access_token():
    # Create an MSAL ConfidentialClientApplication instance
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    
    # Get the token
    result = app.acquire_token_for_client(scopes=["https://database.windows.net/.default"])
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire access token")

# Connection string for SQLAlchemy with Azure SQL using the access token
def create_sqlalchemy_connection():
    access_token = get_access_token()

    # Build the ODBC connection string
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};" \
                        f"Server={SQL_SERVER};" \
                        f"Database={DATABASE_NAME};" \
                        f"Authentication=ActiveDirectoryPassword;" \
                        f"AccessToken={access_token};"

    # Create an engine using SQLAlchemy
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

    return engine

# Example function to query the database
def query_database():
    engine = create_sqlalchemy_connection()

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Example query (replace with your own query)
    result = session.execute("SELECT TOP 5 * FROM your_table")

    # Fetch and print the results
    for row in result:
        print(row)

    session.close()

# Call the query function
if __name__ == "__main__":
    query_database()
