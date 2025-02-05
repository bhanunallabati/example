import pyodbc
import msal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Azure AD and SQL Server details
TENANT_ID = "your-tenant-id"                # Your Azure Tenant ID
CLIENT_ID = "your-client-id"                # Your Azure AD Application (Client) ID
CLIENT_SECRET = "your-client-secret"        # Your Azure AD Application Client Secret
SQL_SERVER = "your-sql-server.database.windows.net"  # Your Azure SQL Server
DATABASE_NAME = "your-database-name"        # Your Azure SQL Database name
USER_NAME = "your-username"                 # Entra ID Username (Azure AD User)
USER_PASSWORD = "your-password"             # Entra ID Password (Azure AD User)

# Get an access token from Azure AD using password-based authentication
def get_access_token_with_password():
    # Create an MSAL ConfidentialClientApplication instance (this is for using client secret)
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )

    # Get the token using the user's username/password
    result = app.acquire_token_by_username_password(
        username=USER_NAME,
        password=USER_PASSWORD,
        scopes=["https://database.windows.net/.default"],
    )

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire access token")

# Create SQLAlchemy engine and establish connection using the Azure SQL access token
def create_sqlalchemy_connection():
    access_token = get_access_token_with_password()

    # Build the ODBC connection string for SQLAlchemy
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};" \
                        f"Server={SQL_SERVER};" \
                        f"Database={DATABASE_NAME};" \
                        f"Authentication=ActiveDirectoryPassword;" \
                        f"AccessToken={access_token};"

    # Create SQLAlchemy engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    
    return engine

# Example function to query the database
def query_database():
    engine = create_sqlalchemy_connection()

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Example query (replace with your actual query)
    result = session.execute("SELECT TOP 5 * FROM your_table")

    # Fetch and print the results
    for row in result:
        print(row)

    session.close()

# Call the query function
if __name__ == "__main__":
    query_database()
