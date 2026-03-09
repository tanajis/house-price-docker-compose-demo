import pandas as pd

# Read the JSON file
# use absolute path inside Airflow container to match mounted volume
json_path = '/opt/airflow/data/house_prices.json'
df = pd.read_json(json_path)

# Save to CSV
csv_path = '/opt/airflow/data/house_prices.csv'
df.to_csv(csv_path, index=False)

print("JSON data has been converted to CSV successfully!")