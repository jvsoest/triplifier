echo "jdbc.url = jdbc:postgresql://localhost:5432/my_database" > test.properties
echo "jdbc.user = postgres" >> test.properties
echo "jdbc.password = postgres" >> test.properties
echo "jdbc.driver = org.postgresql.Driver" >> test.properties

# Run the Java tool 10 times with the test configuration file
for i in $(seq 1 10)
do
    echo "Running iteration $i..."
    { time java -Xmx10g -jar triplifier-1.4.0-SNAPSHOT-jar-with-dependencies.jar -p test.properties; } 2>> time_java.log
    if [ $? -ne 0 ]; then
        echo "Java tool failed to run on iteration $i."
        exit 1
    fi
done

rm test.properties