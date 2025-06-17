#!/bin/bash

# This script is used to test the Python triplifier tool performance time

# install the triplifier tool
pip install triplifier
# Create a test configuration file for the Python tool
echo "db:" > test.yaml
echo "  url: \"postgresql://postgres:postgres@localhost:5432/my_database\"" >> test.yaml

# Run the Python tool 10 times with the test configuration file
for i in $(seq 1 10)
do
    echo "Running iteration $i..."
    { time triplifier -c test.yaml; } 2>> time_python.log
    if [ $? -ne 0 ]; then
        echo "Python tool failed to run on iteration $i."
        exit 1
    fi
done

rm test.yaml