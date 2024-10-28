"""load_sampledata.py"""

import sys
import os
import json

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

# Connect to Kusto Emulator
KUSTO_EMULATOR_URI = "http://localhost:8080"  # assuming default port 8080
DATABASE = "NetDefaultDB"  # default database


def setup_table(client, table_name, schema):
    """A function responsible for formatting and running the create table command."""
    print(f"\nAttempting to create table {table_name}...")
    columns = ", ".join(
        [f"{col['ColumnName']} : {col['ColumnType']}" for col in schema]
    )
    create_table_cmd = f".create table {table_name} ({columns})"
    client.execute(DATABASE, create_table_cmd)
    print(f"Created table {table_name}!")


def ingest_data(client, table_name, data):
    """A function responsible for formatting and running the ingest inline commands."""
    print(f"Attempting to ingest data into {table_name}...")
    for row in data:
        insert_cmd = f".ingest inline into table {table_name} <| {json.dumps(row)}"
        client.execute(DATABASE, insert_cmd)
    print(f"Data ingested into {table_name}!")


def main():
    # Set up Kusto connection
    print("Setting up connection with the ADX cluster...")
    kcsb = KustoConnectionStringBuilder.with_aad_application_token_authentication(
        connection_string=KUSTO_EMULATOR_URI, application_token="123456"
    )

    with KustoClient(kcsb) as client:
        # Load schema and data files
        sample_data_dir = os.path.join(os.getcwd(), "sampledata")
        print(f"\nSearching for sample data in {sample_data_dir}")
        for table_folder in os.listdir(sample_data_dir):
            table_path = os.path.join(sample_data_dir, table_folder)

            # Load schema
            with open(
                os.path.join(table_path, "schema.json"), encoding="utf8"
            ) as schema_file:
                schema = json.load(schema_file)

            # Create table
            setup_table(client, table_folder, schema)

            # Load data
            with open(
                os.path.join(table_path, "data.json"), encoding="utf8"
            ) as data_file:
                data = json.load(data_file)
                ingest_data(client, table_folder, data)
    print("\nDone Loading sample data!")


if __name__ == "__main__":
    sys.stdout.flush()
    main()
