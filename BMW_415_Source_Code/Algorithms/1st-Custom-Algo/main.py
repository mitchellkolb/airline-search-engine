from neo4j import GraphDatabase
from time import time
import cProfile

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

def bfs(city, d):
    with driver.session() as session:
        result = session.run("""
            MATCH (start:Airport {city: $city})
            CALL apoc.path.spanningTree(start, {minLevel: 1, maxLevel: $d, relationshipFilter: "FLIGHT>"})
            YIELD path
            RETURN [node in nodes(path) | node.city] as cities
        """, city=city, d=d)
        return [record["cities"] for record in result]


t0 = time()
bfs("Spokane", 2)
t1 = time()
print('(Spokane, 2) takes %f seconds' %(t1-t0))

t0 = time()
print(bfs("New York", 2))
t1 = time()
print('(New York, 2) takes %f seconds' %(t1-t0))

t0 = time()
print(bfs("Seattle", 1))
t1 = time()
print('(New York, 1) takes %f seconds' %(t1-t0))

t0 = time()
bfs("Portland", 1)
t1 = time()
print('(Portland, 1) takes %f seconds' %(t1-t0))