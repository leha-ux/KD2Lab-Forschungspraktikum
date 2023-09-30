# Importieren Sie die Module tkinter, webbrowser und requests
import tkinter as tk
import tkinter.filedialog as fd
import webbrowser
import requests
import time
import datetime
import random
import sys
from tobii_timescale import startTracking, stopTracking


global serverIP

#Schema um deinProgramm aus tobii_timescale.py zu starten + file_path zur License Datei,da die ja an den einzelnen Pcs verschieden ist.
def startTimescaleDBConnection(file_path): 
    # Try to start the tracking and catch any errors try: 
    try:
        startTracking(serverIP, file_path, mappingID) 
        # Update the label with a success message 
        instruction.config(
        text=f"Tracking started successfully with mapping ID {mappingID}"
        )
    except Exception as e: 
        # Update the label with an error message 
        instruction.config(text=f"Error: {e}")
        
    button4 = tk.Button( frame, text='Stop Tracking', command=lambda: stopTracking(), width=15, height=1, bg='#00a0e9', fg='white', font=('Arial', 12), relief=tk.FLAT, cursor='hand2', ) 
    button4.pack(pady=10)
        
        


def generate_unique_id():
    # Erhalten Sie das aktuelle Datum und die Uhrzeit als String im Format YYYYMMDDHHMMSS
    date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Erzeugen Sie eine zufällige Zahl zwischen 0 und 9999 als String mit vier Stellen
    random_number = str(random.randint(0, 9999)).zfill(4)

    # Verbinden Sie das Datum, die Uhrzeit und die zufällige Zahl mit einem Bindestrich
    unique_id = date_time + "-" + random_number
    
    # Geben Sie die eindeutige ID zurück
    return str(unique_id)

    
# Definieren Sie eine Funktion, die beim Klick auf den Button aufgerufen wird
def button_clicked(input_id):
    
    # Warten Sie, bis der Benutzer eine URL eingegeben hat
    url = f"http://{serverIP}:8000/InitializeParticipant/{input_id}"

    webbrowser.open(url)

    
    # Senden Sie einen GET-Request an die Website mit dem String als Parameter
    response = requests.get(url)

    # Warten Sie 5 Sekunden
    time.sleep(2)

    # Lesen Sie den neuen Link der Website aus
    new_url = response.url
    webbrowser.open(f"{new_url}?string={mappingID}")
    # Update the label with a message that the initialization is done
    instruction.config(text=f"Initialization done. Mapping ID is {mappingID}")
    button2.pack(pady=10) 

    

    
    
def file_clicked():

    # Öffnen Sie einen Dateiauswahldialog und speichern Sie den Pfad zur ausgewählten Datei
    file_path = fd.askopenfilename()

    # Erstellen Sie einen dritten Button, der die Funktion startTimescaleDBConnection aufruft
    button3 = tk.Button(frame, text='Start TimescaleDB Connection', command=lambda: startTimescaleDBConnection(file_path), width=15, height=1, bg='white', fg='black', font=('Arial', 12), relief=tk.FLAT, cursor='hand2')
    button3.pack()



# Define a function to save the input to a text file and assign it to the variable
def save_input():
    # Get the input from the entry widget
    input = entryIP.get()
    global serverIP
    serverIP = input
    # Open a text file in write mode
    file = open("ipAddress.txt", "w")
    # Write the input to the file
    file.write(input)
    # Close the file
    file.close()
    # Assign the input to the variable
    ip_address.set(input)
    # Print a confirmation message
    print("IP address saved and assigned to variable.")
    
    entry.pack(pady=10)
    button.pack(pady=10)  


# Erstellen Sie ein tkinter-Fenster
window = tk.Tk()
window.title("Initialisierung")

window_width = 600 
window_height = 400 
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 
x = (screen_width // 2) - (window_width // 2) 
y = (screen_height // 2) - (window_height // 2) 
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

global mappingID
mappingID= generate_unique_id()


# Erstellen Sie ein zweites Frame am Boden des Fensters
bottom_frame = tk.Frame(window, bg='#f0f0f0')
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

frame = tk.Frame(window, bg='#f0f0f0') 
frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
 
# Create a label to display the question
labelIP = tk.Label(frame, text="Aktuelle IP Adresse? Sonst neue eingeben.")
labelIP.pack(pady=1)

entryIP = tk.Entry(frame, width=40) 
entryIP.insert(0, '')
entryIP.pack(pady=1)

# Create a variable to store the IP address
ip_address = tk.StringVar()

# Create a button to save the input and assign it to the variable
buttonIP = tk.Button(frame, text="Next ", command=save_input, width=5, height=1, bg='white', fg='black', font=('Arial', 12), relief=tk.FLAT, cursor='hand2')
buttonIP.pack(pady=1)

# Try to read the content of the text file and insert it into the entry widget
try:
    # Open the text file in read mode
    file = open("ipAddress.txt", "r")
    # Read the content of the file
    content = file.read()
    # Close the file
    file.close()
    # Insert the content into the entry widget
    entryIP.insert(0, content)
except:
    # If the file does not exist or is empty, insert a default message
    entryIP.insert(0, "Enter Server IP")
    
entry = tk.Entry(frame, width=40) 
entry.insert(0, 'Enter Init Participant ID')
       

                 
# Erstellen Sie einen Button, der die Funktion button_clicked aufruft
button = tk.Button(frame, text='Init', command=lambda: button_clicked(entry.get()), width=15, height=1, bg='#00a0e9', fg='white', font=('Arial', 12), relief=tk.FLAT, cursor='hand2', ) 
button2 = tk.Button(frame, text='Choose File', command=file_clicked, width=15, height=1, bg='#00a0e9', fg='white', font=('Arial', 12), relief=tk.FLAT, cursor='hand2', ) 





# Erstellen Sie ein Text Widget, um den Terminal Output anzuzeigen
console = tk.Text(window, width=40, height=30, bg='white', bd=0)
console.pack(side=tk.RIGHT, padx=10, pady=10)

# Erstellen Sie eine Klasse, die den Text in das Widget schreibt
class Umleitung():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)

# Weise sys.stdout eine Instanz der Umleitungsklasse mit dem Text Widget zu
sys.stdout = Umleitung(console)



# Erstellen Sie ein Label in dem Frame, das eine Anweisung enthält
instruction = tk.Label(bottom_frame, text="Please enter an ID and choose a file.")
instruction.pack()


# Starten Sie die GUI-Schleife
window.mainloop()









