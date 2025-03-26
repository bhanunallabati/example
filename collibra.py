from airflow import DAG
from airflow.providers.collibra.hooks.collibra import CollibraHook
from airflow.operators.python import PythonOperator
from datetime import datetime

class CollibraClient:
    def __init__(self, conn_id="collibra_default"):
        self.hook = CollibraHook(conn_id=conn_id)
    
    def get_assets(self):
        """Fetch assets from Collibra API."""
        endpoint = "asset"
        response = self.hook.run(endpoint)
        return response.json()
    
    def create_asset(self, name, domain_id, type_id):
        """Create a new asset in Collibra."""
        endpoint = "asset"
        payload = {
            "name": name,
            "domainId": domain_id,
            "typeId": type_id
        }
        response = self.hook.run(endpoint, json=payload, method="POST")
        return response.json()

def fetch_collibra_assets(**kwargs):
    client = CollibraClient()
    assets = client.get_assets()
    print("Fetched Assets:", assets)
    return assets

def create_collibra_asset(**kwargs):
    client = CollibraClient()
    asset = client.create_asset(name="Sample Asset", domain_id="12345", type_id="67890")
    print("Created Asset:", asset)
    return asset

# Define the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 26),
    "retries": 1,
}

dag = DAG(
    "collibra_asset_management",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

fetch_assets_task = PythonOperator(
    task_id="fetch_assets",
    python_callable=fetch_collibra_assets,
    provide_context=True,
    dag=dag,
)

create_asset_task = PythonOperator(
    task_id="create_asset",
    python_callable=create_collibra_asset,
    provide_context=True,
    dag=dag,
)

fetch_assets_task >> create_asset_task
