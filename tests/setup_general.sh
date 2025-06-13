#!/bin/bash
cd ../containerTest && sh setupdb.sh

cd ../tests

# Wait for the database to be ready by checking connectivity
until docker exec postgresdb pg_isready -U postgres; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

pip install pandas sqlalchemy psycopg2-binary

# load the data into the PostgreSQL database
python load_data.py