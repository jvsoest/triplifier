import pandas as pd
from sqlalchemy import create_engine
import sys
import os

def csv_to_postgres(csv_file_path, db_url, table_name):
    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Connect to the PostgreSQL database using SQLAlchemy
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            # Write the DataFrame to PostgreSQL
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
            print(f"Table '{table_name}' created and data inserted successfully.")
    except Exception as e:
        print(f"Database error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    # Replace these with your actual values or pass them via arguments
    csv_file_path = 'synthetic_patient_data.csv'  # Path to your CSV file
    db_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/my_database'
    table_name = 'synthethic_patient_data'

    if not os.path.exists(csv_file_path):
        print(f"CSV file '{csv_file_path}' does not exist.")
        sys.exit(1)

    csv_to_postgres(csv_file_path, db_url, table_name)