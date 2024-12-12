import pandas as pd
from sqlalchemy import create_engine
import json
import os
from sqlalchemy.sql import text


# Database configuration
db_config = {
    "hostname": "localhost",
    "username": "postgres",
    "password": "8197",
    "database": "poc_database",
    "port": 5432,
}

# Database connection string
db_url = f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(db_url)

def insert_data_to_db(json_data, table_name):
    
    #Insert JSON data into the database table and Truncate the table before inserting.
    try:
        # Truncate the table
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))
            print(f"Table '{table_name}' truncated successfully.")

        # Convert JSON to DataFrame and insert into the database
        df = pd.DataFrame(json_data)
        with engine.begin() as conn:
            df.to_sql(table_name, con=conn, if_exists="append", index=False)
            print(f"Data inserted into the '{table_name}' table successfully.")
        return True

    except Exception as e:
        print(f"Error while inserting data: {e}")
        return False

def export_data_to_csv(table_name, csv_file):
  
    #Export data from the database table to a CSV file.

    try:
        # Fetch data from the table
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, engine)

        # Check if DataFrame is empty
        if df.empty:
            print("Warning: The DataFrame is empty! No data to export.")
        else:
            df.to_csv(csv_file, index=False)
            print(f"Data successfully written to '{csv_file}'.")
    except Exception as e:
        print(f"Error while exporting data: {e}")

if __name__ == "__main__":
    json_file = "C:/Users/devara/Desktop/python/python_db/student.json"

    # Check if the JSON file exists
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file '{json_file}' not found.")

    # Load JSON data
    with open(json_file, "r") as f:
        json_data = json.load(f)

    table_name = "students"
    csv_file = "student.csv"

    # Insert data and export only if insertion succeeds
    if insert_data_to_db(json_data, table_name):
        export_data_to_csv(table_name, csv_file)
