

from neo4j import GraphDatabase
from time import time
import cProfile

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "loplop123")

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()


def find_connected_route(driver, city_x, city_y):
    def fetch_airports(session, city):
        result = session.run("""
            MATCH (a:Airport {city: $city})
            RETURN a
        """, city=city)

        airports = []
        for record in result:
            airport_node = record["a"]
            airport_data = {
                "name": airport_node["name"],
                "iata": airport_node["iata"],
                "latitude": airport_node["latitude"],
                "longitude": airport_node["longitude"],
            }
            airports.append(airport_data)

        return airports

    with driver.session() as session:
        airports_x = fetch_airports(session, city_x)
        airports_y = fetch_airports(session, city_y)

        routes = []
        route_num = 1
        for airport_x in airports_x:
            for airport_y in airports_y:
                result = session.run("""
                    MATCH p = shortestPath((a:Airport {iata: $iata_x})-[*..15]-(b:Airport {iata: $iata_y}))
                    RETURN p
                """, iata_x=airport_x["iata"], iata_y=airport_y["iata"])

                for record in result:
                    path = record["p"]
                    route_info = [node["name"] for node in path.nodes if "Airport" in node.labels]
                    routes.append(f"Route {route_num}: {route_info[0]} (in {city_x}) to {route_info[-1]} (in {city_y}).")
                    route_num += 1

        return routes


routes = find_connected_route(driver, 'Spokane', 'Seattle')
for route in routes:
    print(route)

