


from neo4j import GraphDatabase
from pyspark.sql import SparkSession
import pandas as pd
from time import time #this is to check the additional time that it takes to execute the custom algo



#username and password
username = "neo4j-451"
password = "password12345"

# Connect to the local Neo4j database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(username, password))

# Verify that the connection is working by running this basic match query
#with driver.session() as session:
#   session.run("MATCH (n) RETURN n LIMIT 1")

print("Above is a test for neo connection. Below is the results")


# Creating a Spark session
spark = SparkSession.builder.appName('custom_algo_2_shortest_path').getOrCreate()


def custom_algo_2_shortest_path(spark, matrix_variable):
   # Initialize the shortest paths matrix by using the weights of the edges in the neo4j graph that we have
   # It should be setup so that if there is no edge between two airports the value in the matrix is NULL
   shortest_paths = matrix_variable.copy()

   # For each pair of airports (i, j) 
   # This tries all three sections of the airport route process
   for k in range(shortest_paths.shape[0]):
       for i in range(shortest_paths.shape[0]):
           for j in range(shortest_paths.shape[0]):
               # Update the shortest travel time
               shortest_paths[i][j] = min(shortest_paths[i][j], shortest_paths[i][k] + shortest_paths[k][j])

   return shortest_paths


"""
I had to add this new realtion type to get this custom algorithm to work effectivley the arrives_at and departs_from wasnt enough I thought.


MATCH (s:Airport), (d:Airport)
WHERE s <> d
CREATE (s)-[:DISTANCE {distance: 1}]->(d);

"""


# Use the Neo4j driver to execute a Cypher query so I can get data from my local db
# This query should get me data that is the distance between each and every pair of airports
with driver.session() as session:
   result = session.run("""
        MATCH (origin:Airport)-[r:DISTANCE]->(destination:Airport)
        WHERE origin.id < destination.id
        RETURN origin.id AS origin_id, destination.id AS destination_id, r.distance AS distance
   """)

# Convert the result to a DataFrame as shown in lecture becuase im using python
matrix_variable = spark.createDataFrame(result.data(), ["origin_id", "destination_id", "distance"])

# Convert the DataFrame to a NumPy array
matrix_variable = matrix_variable.toPandas().values

# Run the algorithm
t0 = time()
shortest_paths = custom_algo_2_shortest_path(spark, matrix_variable)
t1 = time()
print('Algorithm takes %f seconds' %(t1-t0))


# This shoudl print the shortest paths after all the calculations are done in the algo
n = len(shortest_paths)
for i in range(n):
   for j in range(n):
       if i != j:
           print(f"Shortest distance from {i} to {j} is {shortest_paths[i][j]}")


