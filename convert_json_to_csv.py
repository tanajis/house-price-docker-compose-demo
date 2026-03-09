import pandas as pd
import os

# Determine if running in Airflow container or locally
# In Airflow container, AIRFLOW_HOME is set to /opt/airflow
is_airflow_container = os.getenv('AIRFLOW_HOME') == '/opt/airflow'

# Set paths based on environment
if is_airflow_container:
    # Running in Airflow Docker container
    data_dir = '/opt/airflow/data'
else:
    # Running locally
    data_dir = 'data'

# Ensure data directory exists
os.makedirs(data_dir, exist_ok=True)

# Read the JSON file
json_path = os.path.join(data_dir, 'house_prices.json')
print(f"Reading JSON from: {json_path}")
df = pd.read_json(json_path)

# Save to CSV
csv_path = os.path.join(data_dir, 'house_prices.csv')
print(f"Saving CSV to: {csv_path}")
df.to_csv(csv_path, index=False)

print("JSON data has been converted to CSV successfully!")