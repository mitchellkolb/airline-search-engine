from neo4j import GraphDatabase
from functions import *

URI = "bolt://localhost:7687"  # Replace with your actual URI
AUTH = ("neo4j", "loplop123")  # Replace with your actual credentials

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

def menu():
    while True:
        print("\nSearch Engine Menu:")
        print("1. Find list of airports operating in the country X")
        print("2. Find the list of Airlines having X stops")
        print("3. List of airlines operating with code share")
        print("4. Find the list of active airlines in the United States")
        print("5. Exit")
        print("6. Top K cities with most incoming airlines")
        print("7. Top K cities with most outgoing airlines")

        choice = input("Enter your choice: ")
        print("\n")

        if choice == '1':
            pass

        elif choice == '2':
            stops = int(input("Please enter the number of stops: "))
            airlines = find_airlines(driver, stops)
            print("Airlines with", stops, "stops:")
            if not airlines:
                print("\nNo airlines found with " + str(stops) + " stops" )
            for airline in airlines:
                print(airline)
        elif choice == '3':
            # Call the function to list airlines operating with code share
            # list_airlines_code_share()
            pass  # Placeholder to avoid indentation error
        elif choice == '4':
            airlines = find_active_airlines_US(driver)
            print("Active airlines in the United States:")
            for airline in airlines:
                print(airline)

        elif choice == '5':
            print("Exiting...")
            break

        elif choice == '6':
            k = int(input("Please enter the number of top cities you want to see: "))
            cities = top_k_cities_incoming(driver, k)
            print("Top", k, "cities with most incoming airlines:")
            for city, airlines in cities:
                print(city, "with", airlines, "airlines")

        elif choice == '7':
            k = int(input("Please enter the number of top cities you want to see: "))
            cities = top_k_cities_outgoing(driver, k)
            print("Top", k, "cities with most outgoing airlines:")
            for city, airlines in cities:
                print(city, "with", airlines, "airlines")

        elif choice == '8':
            source = "Seattle Tacoma International Airport"
            destination = "Metropolitan Oakland International Airport"
            max_stops = 2
            trip = find_trip(driver, source, destination, max_stops)
            print("Trip from", source, "to", destination, "with less than", max_stops, "stops:")
            if not trip:
                print("\nNo trip found with the given constraints.")
            for path in trip:
                print(path)

        elif choice == '10':
            print(transitive_closure(driver))

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    menu()
