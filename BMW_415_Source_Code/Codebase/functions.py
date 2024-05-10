import matplotlib.pyplot as plt



def find_airlines(driver, airline_name):
  with driver.session() as session:
      result = session.run("""
        MATCH (a:Airline {name: $airline_name})
        RETURN properties(a) as airline_properties""", airline_name=airline_name)

      final = [record["airline_properties"] for record in result]
      print(final)
      return final

    



def find_active_airlines_US(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Airline {country: 'United States', active: 'Y'})
            RETURN a.name
        """)
        print(result)
        return [record["a.name"] for record in result]
    
#BRIAN
def find_top_country_airline(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (flight)-[:DEPARTS_FROM]->(sourceAirport:Airport)
            WITH sourceAirport.city AS city, COUNT(flight) AS numberOfSourceAirports
            ORDER BY numberOfSourceAirports DESC
            LIMIT 10
            RETURN city, numberOfSourceAirports
        """)
        return [(record["city"], record["numberOfSourceAirports"]) for record in result]
#BRIAN

def top_k_cities_incoming(driver, k):
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Route)-[:ARRIVES_AT]->(a:Airport)
            RETURN a.city as city, COUNT(DISTINCT r.airline) as airlines
            ORDER BY airlines DESC
            LIMIT toInteger($k)
        """, k=k)
        data = [(record["city"], record["airlines"]) for record in result]

        cities = [record[0] for record in data]
        airlines = [record[1] for record in data]

        width_px = 500  # Adjusted width in pixels
        height_px = 300  # Adjusted height in pixels
        dpi = 100  # Standard screen resolution in dots per inch

        # Calculate size in inches
        width_inch = width_px / dpi
        height_inch = height_px / dpi

        # Set the figure size and create the bar plot
        plt.figure(figsize=(width_inch, height_inch))
        plt.barh(cities, airlines, color='skyblue')
        plt.xlabel('Number of Airlines')
        plt.title(f'Top {k} Cities by Incoming Airlines')
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest count at the top
        plt.tight_layout()

        # Save the plot to a file
        plt.savefig("plot.png", dpi=dpi, bbox_inches='tight')  # Use bbox_inches='tight'
        plt.close()  # Close the plot to avoid displaying it

        return data


def top_k_cities_outgoing(driver, k):
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Route)-[:DEPARTS_FROM]->(a:Airport)
            RETURN a.city as city, COUNT(DISTINCT r.airline) as airlines
            ORDER BY airlines DESC
            LIMIT toInteger($k)
        """, k=k)
        data = [(record["city"], record["airlines"]) for record in result]

        cities = [record[0] for record in data]
        airlines = [record[1] for record in data]

        width_px = 500  # Adjusted width in pixels
        height_px = 300  # Adjusted height in pixels
        dpi = 100  # Standard screen resolution in dots per inch

        # Calculate size in inches
        width_inch = width_px / dpi
        height_inch = height_px / dpi

        # Set the figure size and create the bar plot
        plt.figure(figsize=(width_inch, height_inch))
        plt.barh(cities, airlines, color='skyblue')
        plt.xlabel('Number of Airlines')
        plt.title(f'Top {k} Cities by Outgoing Airlines')
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest count at the top
        plt.tight_layout()

        # Save the plot to a file
        plt.savefig("plot.png", dpi=dpi, bbox_inches='tight')  # Use bbox_inches='tight'
        plt.close()  # Close the plot to avoid displaying it

        return data


def find_trip(driver, X, Y, Z):
    with driver.session() as session:
        result = session.run(f"MATCH (a:Airport {{name: '{X}'}})-[:DEPARTS_FROM*..{Z}]-(b:Airport {{name: '{Y}'}}) RETURN a, b")
        return result.data()


def transitive_closure(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (start:Airport)-[:DEPARTS_FROM]->(middle:Airport)<-[:ARRIVES_AT]-(end:Airport)
            WITH start, end
            MATCH path = (start)-[:ARRIVES_AT*]->(end)
            RETURN path
        """)
        return [record["path"] for record in result]

def get_cities_within_d_hops(city, d, driver):
   with driver.session() as session:
       result = session.run("""
           MATCH (start:Airport {city: $city})
           CALL apoc.path.spanningTree(start, {maxLevel: $d, bfs: true})
           YIELD path
           RETURN path
       """, city=city, d=d)

       cities = set() # Using a set to avoid duplicate city names

       for record in result:
           path = record['path']
           nodes = path.nodes
           for node in nodes:
               if 'city' in node:
                  cities.add(node['city'])

       return list(cities)


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



#This one is the function shown in the presentation.
def shortest_path_old(driver, airport1, airport2):
  with driver.session() as session:
      result = session.run("""
          MATCH (a1:Airport {name: $airport1}), (a2:Airport {name: $airport2})
          CALL apoc.algo.shortestPath(a1, a2, 'DEPARTS_FROM,ARRIVES_AT')
          YIELD path
          RETURN path
      """, airport1=airport1, airport2=airport2)

      paths = []
      for record in result:
          path = [node.name for node in record["path"]]
          paths.append(path)
      return paths


#This is the new shortest_path function that uses PySpark as requested by the professor
def shortest_path(driver, airport1, airport2):
    from pyspark.sql import SparkSession
    from neo4j import GraphDatabase
    from graphframes import GraphFrame

    spark = SparkSession.builder.getOrCreate()

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

    #get data needed from the database
    def get_data(driver):
        with driver.session() as session:
            result = session.run("""
                MATCH (a:Airport), (b:Airport)
                WHERE a <> b
                RETURN a.name AS src, b.name AS dst
            """)

            data = []
            for record in result:
                data.append(record)

        return data

    data = get_data(driver)

    vertices = spark.createDataFrame(data, ["src", "dst"])
    edges = vertices.withColumnRenamed("src", "src").withColumnRenamed("dst", "dst")
    graph = GraphFrame(vertices, edges)

    shortest_paths = graph.shortestPaths(sourceId="src", targetId="dst", edgeWeight="distance")

    #I want the result as a list so I need to get it in the right context
    result = shortest_paths.collect()
    spark.stop()

    return result









