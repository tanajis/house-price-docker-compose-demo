#!/usr/bin/env python3
"""
Script to generate a Fernet key dynamically for Airflow encryption.
This script generates a new Fernet key and writes it to a .env file
for use in docker-compose.yml.
"""

from cryptography.fernet import Fernet
import os

def generate_fernet_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key().decode()

def main():
    # Generate the key
    fernet_key = generate_fernet_key()

    # Write to .env file
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_file_path, 'w') as f:
        f.write(f'AIRFLOW__CORE__FERNET_KEY={fernet_key}\n')

    print(f"Fernet key generated and saved to {env_file_path}")
    print(f"Key: {fernet_key}")

if __name__ == "__main__":
    main()