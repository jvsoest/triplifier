import pandas as pd
from sqlalchemy import create_engine
import sys
import os

def csv_to_postgres(csv_file_path, db_url, table_name):
    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8')
        # limit DF to 1500 columns
        if df.shape[1] > 1500:
            df = df.iloc[:, :1500]
        # fix issue of e.g. 9,11E+10 into a float
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].str.contains(r'^\d+,\d+E\+\d+$', na=False).any():
                df[col] = df[col].str.replace(',', '.').astype(float)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    print(f"CSV file '{csv_file_path}' read successfully with {df.shape[0]} rows and {df.shape[1]} columns.")

    # Connect to the PostgreSQL database using SQLAlchemy
    try:
        engine = create_engine(db_url)
        # Write the DataFrame to PostgreSQL
        if len(df) > 5000:
            for start in range(0, len(df), 5000):
                end = start + 5000
                print(f"Inserting rows {start} to {end} into table '{table_name}'...")
                df.iloc[start:end].to_sql(table_name, con=engine, if_exists='append' if start > 0 else 'replace', index=False)
        else:
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
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