

import PySimpleGUI as sg # pip install pysimplegui
from neo4j import GraphDatabase #pip install neo4j
from functions import *
#from tests import *

#form bfs import *
#from shortest_path import *

sg.theme('Dark Blue 3')

def connectToDB(values):
    global driver #Allows me to use in the searchScreen() window
    URI = values['-URI-']
    user = values['-USER-']
    passw = values['-PASS-']
    AUTH = (user, passw)

    print(f"URI: {URI}, User: {user}, Password: {passw}")
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()   
    



def option1(): #Placeholder function
    return("Yes")



def searchScreen():
  options = ["Find Airline Details", "Find Active Airlines in the US", "Top k Cities Incoming", "Top k Cities Outgoing", "Shortest Path Algorithm", "Cities Within d Hops", "Which country(or)territory has the highest number of airports", "Find Connected Route"] #"Find Trip", "Transitive Closure",

  layout_SearchEngine = [
      [sg.Text('')],
      [sg.Text('BMW - Airline Search Engine Project', font='_ 14', justification='c', expand_x=True)],
      [sg.Text('')],
      [sg.Column([[sg.OptionMenu(options, options[0], key='-OPTION-'), sg.Button('| Search |',)]], justification='c')],
      [sg.Text('')],
      [sg.HSep()],
      [sg.Text('')],
      [sg.Text(''), sg.Text('', visible=False, key='-INFOTEXT-'), sg.Input("", size=(10,1), visible=False, key='-FIRST-'), sg.Input("", size=(10,1), visible=False, key='-SECOND-'), sg.Input("", size=(10,1), visible=False, key='-THIRD-'), sg.Button('Enter', visible=False)],
      [sg.Text(''), sg.Multiline(size=(89,13), disabled=True, visible=False, key='-OUTPUT-')],
      [sg.Text(''), sg.Image(filename='', key='-IMAGE-', size=(400, 400)), sg.Multiline(size=(89, 16), disabled=True, visible=False, key='-OUTPUT-')],
  ]
  search_window = sg.Window('CptS 415 - BMW - Airline Search Engine', layout_SearchEngine, size=(900, 800))



  response = "" #Needs to be declared outside of while scope to use correctly

  while True:
    event, values = search_window.read()
    if event == sg.WINDOW_CLOSED:
        search_window.close()
        break
    if event == '| Search |':
        selected_option = values['-OPTION-']
        # Remove the previous image, if displayed
        search_window['-IMAGE-'].update(filename='')
        if selected_option == "Find Airline Details":
            search_window['-OUTPUT-'].update(visible=False)
            search_window['-INFOTEXT-'].update(visible=True, value="Enter the name of the airport")
            search_window['-FIRST-'].update(visible=True)
            search_window['-SECOND-'].update(visible=False)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)

        elif selected_option == "Find Active Airlines in the US":
            search_window['-INFOTEXT-'].update(visible=False)
            search_window['-FIRST-'].update(visible=False)
            search_window['-SECOND-'].update(visible=False)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=False)
            response = find_active_airlines_US(driver)
            search_window['-OUTPUT-'].update(visible=True, value=response)

        elif selected_option == "Top k Cities Incoming":
            search_window['-OUTPUT-'].update(visible=False)
            search_window['-INFOTEXT-'].update(visible=True, value="Enter a Number")
            search_window['-FIRST-'].update(visible=True)
            search_window['-SECOND-'].update(visible=False)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)

        elif selected_option == "Top k Cities Outgoing":
            search_window['-OUTPUT-'].update(visible=False)
            search_window['-INFOTEXT-'].update(visible=True, value="Enter a Number")
            search_window['-FIRST-'].update(visible=True)
            search_window['-SECOND-'].update(visible=False)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)

        # elif selected_option == "Find Trip":
        #     search_window['-OUTPUT-'].update(visible=False)
        #     search_window['-INFOTEXT-'].update(visible=True, value="Enter a Number")
        #     search_window['-FIRST-'].update(visible=True)
        #     search_window['-SECOND-'].update(visible=True)
        #     search_window['-THIRD-'].update(visible=True)
        #     search_window['Enter'].update(visible=True)

        # elif selected_option == "Transitive Closure":
        #     search_window['-INFOTEXT-'].update(visible=False)
        #     search_window['-FIRST-'].update(visible=False)
        #     search_window['-SECOND-'].update(visible=False)
        #     search_window['-THIRD-'].update(visible=False)
        #     search_window['Enter'].update(visible=False)
        #     response = transitive_closure(driver)
        #     search_window['-OUTPUT-'].update(visible=True, value=response)

        elif selected_option == "Shortest Path Algorithm":
            search_window['-INFOTEXT-'].update(visible=True, value="Enter the name of two airports")
            search_window['-FIRST-'].update(visible=True)
            search_window['-SECOND-'].update(visible=True)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)
            #This is currently being worked on
            #response = shortest_path(driver, )
            search_window['-OUTPUT-'].update(visible=False, value=response)

        elif selected_option == "Cities Within d Hops":
            search_window['-INFOTEXT-'].update(visible=True, value="Enter a city and the number of hops")
            search_window['-FIRST-'].update(visible=True, value="City")
            search_window['-SECOND-'].update(visible=True, value="# of hops")
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)
        ##BRIAN JOO
        elif selected_option == "Which country(or)territory has the highest number of airports":
            search_window['-INFOTEXT-'].update(visible=False)
            search_window['-FIRST-'].update(visible=False)
            search_window['-SECOND-'].update(visible=False)
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=False)
            response = find_top_country_airline(driver)# this is the function i need to manipulate
            search_window['-OUTPUT-'].update(visible=True, value=response)

        elif selected_option == "Find Connected Route":
            search_window['-OUTPUT-'].update(visible=False)
            search_window['-INFOTEXT-'].update(visible=True, value="Enter two cities")
            search_window['-FIRST-'].update(visible=True, value="City 1")
            search_window['-SECOND-'].update(visible=True, value="City 2")
            search_window['-THIRD-'].update(visible=False)
            search_window['Enter'].update(visible=True)

        ########BRIAN JOO
    elif event == "Enter":
        #BRIAN JOO
        selected_option = values['-OPTION-']
        if selected_option == "Which country(or)territory has the highest number of airports":
            stops = values['-FIRST-']
            response =find_top_country_airline(driver)# this is the function i need to manipulate
            search_window['-OUTPUT-'].update(visible=True, value=(response))
        #BRIAN JOO

        selected_option = values['-OPTION-']
        if selected_option == "Find Airline Details":
            airlineName = values['-FIRST-']
            response = find_airlines(driver, airlineName)
            search_window['-OUTPUT-'].update(visible=True, value=(response))

        if selected_option == "Top k Cities Incoming":
            k = values['-FIRST-']
            response = top_k_cities_incoming(driver, k)
            # Update the Image element to display the image file
            search_window['-IMAGE-'].update(filename='plot.png')
            search_window['-OUTPUT-'].update(visible=True, value=(response))

        if selected_option == "Top k Cities Outgoing":
            k = values['-FIRST-']
            response = top_k_cities_outgoing(driver, k)
            # Update the Image element to display the image file
            search_window['-IMAGE-'].update(filename='plot.png')
            search_window['-OUTPUT-'].update(visible=True, value=(response))

        if selected_option == "Shortest Path Algorithm":
            airport1 = values['-FIRST-']
            airport2 = values['-SECOND-']
            response = shortest_path(driver, airport1, airport2)
            search_window['-OUTPUT-'].update(visible=True, value=(response))
        if selected_option == "Cities Within d Hops":
            city = values['-FIRST-']
            d = values['-SECOND-']
            response = get_cities_within_d_hops(city, d, driver)
            search_window['-OUTPUT-'].update(visible=True, value=response)
        if selected_option == "Find Connected Route":
            city_x = values['-FIRST-']
            city_y = values['-SECOND-']
            response = find_connected_route(driver, city_x, city_y)

            # Create a string with all routes concatenated
            routes_display = '\n'.join(response)

            # Update the output window with the routes
            search_window['-OUTPUT-'].update(visible=True, value=routes_display)

        search_window['-INFOTEXT-'].update(visible=False)
        search_window['-FIRST-'].update(visible=False)
        search_window['-SECOND-'].update(visible=False)
        search_window['-THIRD-'].update(visible=False)
        search_window['Enter'].update(visible=False)
        search_window['-OUTPUT-'].update(visible=True, value=response)






layout_ConnectToDB = [[sg.Text('')],
         [sg.Text('BMW - Airline Search Engine Project', font='_ 14', justification='c', expand_x=True)],

         [sg.Text('')],
         [sg.Text(' Neo4j Database Connection:')],
         [sg.Column([[sg.Text('Enter URI:'), sg.Input("bolt://localhost:7687", key='-URI-')]], justification='l')],
         [sg.Column([[sg.Text('Enter AUTH Username:'), sg.Input("neo4j", key='-USER-')]], justification='l')],
         [sg.Column([[sg.Text('Enter AUTH Password:'), sg.Input("12345678", key='-PASS-')]], justification='l')],
         [sg.Button('Connect'), sg.Text('', key='-CONNECT-STATUS-', text_color='white')],
         [sg.Button('Go to Search Engine')]]



window_size = (700, 300)
start_window = sg.Window('CptS 415 - BMW - Airline Search Engine', layout_ConnectToDB, size=window_size)

searchToggle = False

while True: # Event Loop
    event, values = start_window.read()
    if event == sg.WIN_CLOSED:
        start_window.close()
        break
    if event == "Connect":
       try:
           connectToDB(values)
           searchToggle = True
           start_window['-CONNECT-STATUS-'].update("Connected", text_color='light green')
       except Exception as e:
           print(f"Failed to connect to the database: {e}")
           searchToggle = False
           start_window['-CONNECT-STATUS-'].update("Failed to connect", text_color='red')
    if event == 'Go to Search Engine' and searchToggle == True:
        start_window.close()
        searchScreen()





