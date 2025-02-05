import pyodbc
from sqlalchemy import create_engine
from azure.identity import ManagedIdentityCredential
from sqlalchemy.orm import sessionmaker

# Azure SQL Server details
SQL_SERVER = "your-sql-server.database.windows.net"
DATABASE_NAME = "your-database-name"
MANAGED_IDENTITY_CLIENT_ID = "your-managed-identity-client-id"  # Optional: If you need a specific managed identity

# Get an access token using Managed Identity
def get_access_token_using_managed_identity():
    # Create a ManagedIdentityCredential instance
    credential = ManagedIdentityCredential(client_id=MANAGED_IDENTITY_CLIENT_ID)  # optional if using default
    token = credential.get_token("https://database.windows.net/.default")
    
    return token.token

# Create SQLAlchemy engine using the access token
def create_sqlalchemy_connection():
    access_token = get_access_token_using_managed_identity()

    # Build the ODBC connection string for SQLAlchemy
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};" \
                        f"Server={SQL_SERVER};" \
                        f"Database={DATABASE_NAME};" \
                        f"Authentication=ActiveDirectoryMsi;" \
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
