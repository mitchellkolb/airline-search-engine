
#import PySimpleGUI as sg #pip install pysimplegui


"""
menu_def = [['File', ['Open', 'Save', 'Exit']],
           ['Edit', ['Paste', ['Special', 'Normal', 'Hidden']]],
           ['Settings', ['Option &1', 'Option &2', 'Option &3']],
           ['About', '&Help']]


layout = [[sg.Menu(menu_def)],
         [sg.Listbox(values=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], size=(20, 5), key='-LIST-')],
         [sg.Multiline(size=(40, 20), key='-OUTPUT-')]]


window = sg.Window('Window Title', layout)

while True:
   event, values = window.read()
   if event == sg.WINDOW_CLOSED:
       break
   elif event == '-LIST-':
       window['-OUTPUT-'].update(f'You selected {values["-LIST-"][0]}')

window.close()
"""
















"""
sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(12,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # change the "output" element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()

"""





"""

#This give me a window of all avaliable widegts to use when making the UI
def make_window(theme='Topanga'):
   sg.theme(theme)
   treedata = sg.TreeData()
   treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
   treedata.Insert("", '_B_', 'B', [])
   treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
   layout_l = [
               [sg.Text('Text'), sg.Text('Text')],
               [sg.Text('Input'), sg.Input(s=15)],
               [sg.Text('Multiline'), sg.Multiline(s=(15,2))],
               [sg.Text('Output'), sg.Output(s=(15,2))],
               [sg.Text('Combo'), sg.Combo(sg.theme_list(), default_value=sg.theme(), s=(15,22), enable_events=True, readonly=True, k='-COMBO-')],
               [sg.Text('OptionMenu'), sg.OptionMenu(['OptionMenu',],s=(15,2))],
               [sg.Text('Checkbox'), sg.Checkbox('Checkbox')],
               [sg.Text('Radio'), sg.Radio('Radio', 1)],
               [sg.Text('Spin'), sg.Spin(['Spin',], s=(15,2))],
               [sg.Text('Button'), sg.Button('Button')],
               [sg.Text('ButtonMenu'), sg.ButtonMenu('ButtonMenu', sg.MENU_RIGHT_CLICK_EDITME_EXIT)],
               [sg.Text('Slider'), sg.Slider((0,10), orientation='h', s=(10,15))],
               [sg.Text('Listbox'), sg.Listbox(['Listbox', 'Listbox 2'], no_scrollbar=True, s=(15,2))],
               [sg.Text('Image'), sg.Image(sg.EMOJI_BASE64_HAPPY_THUMBS_UP)],
               [sg.Text('Graph'), sg.Graph((125, 50), (0,0), (125,50), k='-GRAPH-')] ]
   layout_r = [[sg.Text('Canvas'), sg.Canvas(background_color=sg.theme_button_color()[1], size=(125,40))],
               [sg.Text('ProgressBar'), sg.ProgressBar(100, orientation='h', s=(10,20), k='-PBAR-')],
               [sg.Text('Table'), sg.Table([[1,2,3], [4,5,6]], ['Col 1','Col 2','Col 3'], num_rows=2)],
               [sg.Text('Tree'), sg.Tree(treedata, ['Heading',], num_rows=3)],
               [sg.Text('Horizontal Separator'), sg.HSep()],
               [sg.Text('Vertical Separator'), sg.VSep()],
               [sg.Text('Frame'), sg.Frame('Frame', [[sg.Text(s=15)]])],
               [sg.Text('Column'), sg.Column([[sg.Text(s=15)]])],
               [sg.Text('Tab, TabGroup'), sg.TabGroup([[sg.Tab('Tab1',[[sg.Text(s=(15,2))]]), sg.Tab('Tab2', [[]])]])],
               [sg.Text('Pane'), sg.Pane([sg.Col([[sg.Text('Pane 1')]]), sg.Col([[sg.Text('Pane 2')]])])],
               [sg.Text('Push'), sg.Push(), sg.Text('Pushed over')],
               [sg.Text('VPush'), sg.VPush()],
               [sg.Text('Sizer'), sg.Sizer(1,1)],
               [sg.Text('StatusBar'), sg.StatusBar('StatusBar')],
               [sg.Text('Sizegrip'), sg.Sizegrip()] ]
   layout = [[sg.Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]], k='-CUST MENUBAR-',p=0)],
             [sg.Text('PySimpleGUI Elements - Use Combo to Change Themes', font='_ 14', justification='c', expand_x=True)],
             [sg.Checkbox('Use Custom Titlebar & Menubar', enable_events=True, k='-USE CUSTOM TITLEBAR-', p=0)],
             [sg.Col(layout_l, p=0), sg.Col(layout_r, p=0)]]
   window = sg.Window('The PySimpleGUI Element List', layout, finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True)
   window['-PBAR-'].update(30)                                                 
   window['-GRAPH-'].draw_image(data=sg.EMOJI_BASE64_HAPPY_JOY, location=(0,50))  
   return window

window = make_window()
while True:
   event, values = window.read()
   if event == sg.WIN_CLOSED or event == 'Exit':
       break
   if event == 'Edit Me':
       sg.execute_editor(__file__)
   if values['-COMBO-'] != sg.theme():
       sg.theme(values['-COMBO-'])
       window.close()
       window = make_window()
   if event == '-USE CUSTOM TITLEBAR-':
       use_custom_titlebar = values['-USE CUSTOM TITLEBAR-']
       sg.set_options(use_custom_titlebar=use_custom_titlebar)



"""












"""
import PySimpleGUI as sg

sg.theme('DarkBlue3')

layout = [
    [sg.Text('Enter your name:'), sg.Input(key='-NAME-')],
    [sg.Text('Enter your age:'), sg.Input(key='-AGE-')],
    [sg.Button('Show'), sg.Button('Exit')],
    [sg.Text(size=(30, 1), key='-OUTPUT-')]
]

window = sg.Window('Input Box Example', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Show':
        name = values['-NAME-']
        age = values['-AGE-']

        # Assign the user-inputted values to variables and print to the screen
        output_text = f"Hello, {name}! You are {age} years old."
        window['-OUTPUT-'].update(output_text)

window.close()
"""









"""
#This creates a blank window then when continue is clicks opens a new window to enter name
import PySimpleGUI as sg

# Start Screen
start_layout = [[sg.Text('Welcome to the program')],
              [sg.Button('Continue')]]
start_window = sg.Window('Start Screen', start_layout, size=(700, 500))

while True:
  event, values = start_window.read()
  if event == sg.WINDOW_CLOSED or event == 'Continue':
      break
start_window.close()

# Name Input Screen
name_layout = [[sg.Text('Please enter your name')],
             [sg.Input(key='-NAME-')],
             [sg.Button('Submit')]]
name_window = sg.Window('Name Input', name_layout, size=(700, 500))

while True:
  event, values = name_window.read()
  if event == sg.WINDOW_CLOSED or event == 'Submit':
      print('Hello, ' + values['-NAME-'])
      break
name_window.close()
"""





"""
#This creates a window then and only when you click continute does it move onto the next window page
import PySimpleGUI as sg


def nextScreen():
    # Name Input Screen
    name_layout = [[sg.Text('Please enter your name')],
                [sg.Input(key='-NAME-')],
                [sg.Button('Submit')]]
    name_window = sg.Window('Name Input', name_layout, size=(700, 500))

    while True:
        event, values = name_window.read()
        if event == sg.WINDOW_CLOSED or event == 'Submit':
            print('Hello, ' + values['-NAME-'])
            break
    name_window.close()

# Start Screen
start_layout = [[sg.Text('Welcome to the program')],
             [sg.Button('Continue')]]
start_window = sg.Window('Start Screen', start_layout, size=(700, 500))

while True:
 event, values = start_window.read()
 if event == 'Continue':
     start_window.close()
     nextScreen()
 if event == sg.WINDOW_CLOSED:
    start_window.close()
    break
"""





"""
#5+ TAB creator

import PySimpleGUI as sg

tab_keys = ['Tab 1']
layout = [[sg.TabGroup([[sg.Tab('Tab 1', [[sg.Text('Tab 1 content')]])]], key='TabGroup')],
          [sg.Button('Add Tab')]]

window = sg.Window('Title', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Add Tab':
        # Add 5 tabs at once
        for i in range(5):
            tab_number = len(tab_keys) + 1
            tab_key = f'Tab {tab_number}'
            window['TabGroup'].add_tab(sg.Tab(tab_key, [[sg.Text(f'Tab {tab_number} content')]]))
            tab_keys.append(tab_key)

window.close()

"""



"""
import PySimpleGUI as sg # pip install pysimplegui

sg.theme('Dark Blue 3')

# Define the size for the name
NAME_SIZE = 30

def name(name):
  dots = NAME_SIZE-len(name)-2
  return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Helvetica 10')

tab_keys = ['Tab 1']
tab_layout = [[sg.Text('Tab 1 content')]]
tab_group = [[sg.TabGroup([[sg.Tab('Tab 1', tab_layout)]], key='TabGroup')]]

layout = [[sg.Text('')],
         [sg.Text('BMW - Airline Search Engine Project', font='_ 14', justification='c', expand_x=True)],
         [sg.Text('Neo4j Database Connection:')],
         [sg.Column([[name('Enter URI:'), sg.Input("bolt", key='-URI-')]], justification='c')],
         [sg.Column([[name('Enter AUTH Username:'), sg.Input(key='-USER-')]], justification='c')],
         [sg.Column([[name('Enter AUTH Password:'), sg.Input(key='-PASS-')]], justification='c')],
         [sg.Text('')],
         [sg.Text('Your typed chars appear here:'), sg.Text(size=(12,1), key='-OUTPUT-')],
         [sg.Input(key='-IN-')],
         [sg.Button('Show'), sg.Button('Exit')], 
         [sg.Text('')],] + tab_group + [[sg.Button('Add Tab')]]



window_size = (700, 700)
window = sg.Window('CptS 415 - BMW - Airline Search Engine', layout, size=window_size)

while True: # Event Loop
   event, values = window.read()
   if event == sg.WIN_CLOSED or event == 'Exit':
       break
   if event == 'Show':
       # change the "output" element to be the value of "input" element
       window['-OUTPUT-'].update(values['-IN-'])
   elif event == 'Add Tab':
       # Add 5 tabs at once
       for i in range(5):
           tab_number = len(tab_keys) + 1
           tab_key = f'Tab {tab_number}'
           window['TabGroup'].add_tab(sg.Tab(tab_key, [[sg.Text(f'Tab {tab_number} content')]]))
           tab_keys.append(tab_key)


window.close()

"""

