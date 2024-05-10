

import csv
from neo4j import GraphDatabase
import numpy as np
import random
import pandas as pd

import re
#df = pd.read_csv('fd.csv')
df = pd.read_csv('routes.csv')
# print(df)
# df = df.replace(r'[<%]', '', regex=True)MATCH (n) DETACH DELETE n;
##df = df.replace(r'\D+', '', regex=True)
#df = df.replace(r'[^\w\s]|_', '', regex=True)
airline_list = df.values.tolist()


transaction_execution_commands = []
# Function to escape single quotes


for i in airline_list:
    # Escape single quotes in the airline_name and airport_name fields
   # for x in range(len(airline_list)):
    #    r = '[@_!#$%^&*()<>?/\|}{~:\']'

    #   i[x] = re.sub(r, '', i[x])

    neo4j_create_statemenet = (
        "CREATE (t:Airline {"
        "`airline`: '" + str(i[0]) + "', "
        "`source airport`: '" + str(i[1]) + "', "
        "`destination airport`: '" + str(i[2]) + "', "
        "`codeshare`: '" + str(i[3]) + "', "
        "`stops`: " + str(i[4]) + ", "
        "`equipment`: '" + str(i[5]) + "'"
        "})"
    )
    transaction_execution_commands.append(neo4j_create_statemenet)


def execute_transactions(transaction_execution_commands):
    data_base_connection = GraphDatabase.driver(
        uri="bolt://localhost:7687", auth=("neo4j", "password"))
    session = data_base_connection.session()
    for i in transaction_execution_commands:
        session.run(i)  # initial db

    for i in airline_list:
        airline_name = str(i[0])
        source_airport = str(i[1])
        destination_airport = str(i[2])

        # Create airline nodes
        session.run(
            "MERGE (a:Airline {`airline`: $airline_name})",
            airline_name=airline_name
        )

        # Create airports and relationships
        session.run(
            "MERGE (source:Airport {`source airport`: $source_airport})",
            source_airport=source_airport
        )

        session.run(
            "MERGE (destination:Airport {`destination airport`: $destination_airport})",
            destination_airport=destination_airport
        )

        # Create relationships between airlines and airports
        session.run(
            "MATCH (a:Airline {`airline`: $airline_name}), (source:Airport {`source airport`: $source_airport}), (destination:Airport {`destination airport`: $destination_airport}) "
            "MERGE (a)-[:OPERATES_AT]->(source) "
            "MERGE (a)-[:OPERATES_AT]->(destination)",
            airline_name=airline_name,
            source_airport=source_airport,
            destination_airport=destination_airport
        )


# the edges should be the routes
execute_transactions(transaction_execution_commands)
