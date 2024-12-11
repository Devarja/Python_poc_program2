import pandas as pd
from sqlalchemy import create_engine
import json
import os
#db configuration
db_config={
    "hostname":"localhost",
    "username":"postgres",
    "password":"8197",
    "database":"poc_database",
    "port":5432,
    }

#database connection to python using create engine
db_url = f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(db_url)

#loading the data from json file
json_file = "C:/Users/devara/Desktop/python/python_db/student.json"

# Check if the file exists
if not os.path.exists(json_file):
    raise FileNotFoundError(f"JSON file '{json_file}' not found.")
else:
    print(f"JSON file found at: {json_file}")

with open(json_file,"r") as f:
    json_data=json.load(f)

#converting json data to dataframe
df=pd.DataFrame(json_data)

#inserting this data to db using pandas
table_name="students"
try:
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    print(f"Data inserted into the '{table_name}' table successfully.")
except Exception as e:
    print(f"Error while inserting data: {e}")

#inserting the db data to csv file
query = "SELECT * FROM students;"  # Modify this based on your table
df_from_db = pd.read_sql_query(query, engine)

# Print the DataFrame
print("Data fetched from the database:")
print(df_from_db)

# Check if DataFrame is empty
if df_from_db.empty:
    print("Warning: The DataFrame is empty!")
else:
    # Write DataFrame to CSV
    csv_file = "student.csv"
    df_from_db.to_csv(csv_file, index=False)
    print(f"Data successfully written to '{csv_file}'.")