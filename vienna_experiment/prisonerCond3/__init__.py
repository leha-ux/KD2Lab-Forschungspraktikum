from otree.api import *
from otree.api import Page
from threading import Timer
import datetime
import psycopg2
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import find_intermediate_color, hex_to_rgb
import random
from random import *
import pandas as pd

doc = """
prisoner
"""

connection = "postgres://postgres:password@localhost:5432/riro2023"

#connect to Timescale database using the psycopg2 connect function
conn = psycopg2.connect(connection)
conn.autocommit = True

class C(BaseConstants):
    NAME_IN_URL = 'cSzenario1'
    PLAYERS_PER_GROUP = 2

    # this is the number of supergames
    NUM_ROUNDS = 3
    STOPPING_PROBABILITY = 1

    PAYOFFA = cu(10)
    PAYOFFB = cu(5)
    PAYOFFC = cu(2)
    PAYOFFD = cu(0)

    # True is cooperate, False is defect
    PAYOFF_MATRIX = {
        (True, True): (PAYOFFB, PAYOFFB),
        (True, False): (PAYOFFD, PAYOFFA),
        (False, True): (PAYOFFA, PAYOFFD),
        (False, False): (PAYOFFC, PAYOFFC),
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


def live_method(player, data):
    group = player.group
    my_id = player.id_in_group

    
    

    
    if group.finished_sg:
        return {my_id: dict(finished_sg=True)}

    [game] = Game.filter(group=group, iteration=group.iteration)

    coop_field = 'coop{}'.format(my_id)

    if 'coop' in data:
        coop = data['coop']
        if getattr(game, coop_field) is not None:
            return
        setattr(game, coop_field, coop)
        coops = (game.coop1, game.coop2)
        is_ready = None not in coops
        if is_ready:
            p1, p2 = group.get_players()
            [game.payoff1, game.payoff2] = C.PAYOFF_MATRIX[coops]
            p1.payoff += game.payoff1
            p2.payoff += game.payoff2

            game.has_results = True
            group.iteration += 1

            # random stopping rule
            if random() < C.STOPPING_PROBABILITY:
                group.finished_sg = True
                return {0: dict(finished_sg=True)}

            Game.create(group=group, iteration=group.iteration)

            return {
                0: dict(should_wait=False, last_results=to_dict(game), iteration=group.iteration)
            }
            
    if 'mappingData' in data:
        #Player 1 without AOIvisualization needs to send his payoutmatrix position data to Player B
        other = player.get_others_in_group()[0]
        other.participant.vars["mappingDATA"] = data['mappingData']

    
    
    
    if 'graph' in data:
        
        
        player.participant.vars["graph"] = getAOI_Visualization()
        df_gaze = getGazeData(player)
        # Rufen Sie die Funktion mit dem gegebenen Dictionary und den x- und y-Werten auf
        trackedAOI = mappingGazeData(player.participant.vars["mappingDATA"], df_gaze)
            
        # Geben Sie das Ergebnis aus
        if trackedAOI:
            print(f"Der Blick liegt in Feld - {trackedAOI} -.")
        else:
            print("Der Blick liegt in keinem Feld.")
                
        updateAOI_Visualization(player, trackedAOI)
        
        return {0: dict(graph=player.participant.vars["graph"].to_json())}
    
    i_decided = getattr(game, coop_field) is not None
    if group.iteration > 0:
        [prev_game] = Game.filter(group=group, iteration=group.iteration - 1)
        last_results = to_dict(prev_game)
    else:
        last_results = None
    return {
        
        my_id: dict(
            should_wait=i_decided and not game.has_results,
            last_results=last_results,
            iteration=group.iteration,
        )
    }


class Game(ExtraModel):
    group = models.Link(Group)
    iteration = models.IntegerField()
    coop1 = models.CurrencyField()
    coop2 = models.CurrencyField()
    payoff1 = models.CurrencyField()
    payoff2 = models.CurrencyField()
    has_results = models.BooleanField(initial=False)


def to_dict(game: Game):
    return dict(payoffs=[game.payoff1, game.payoff2], coops=[game.coop1, game.coop2])


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    
    #Create PupilDilation Visualization for each Player 
    def get_plot(self):
        self.participant.vars["graph"] = getAOI_Visualization()
        aoiVisualization = self.participant.vars["graph"].to_json()
        #Use a list of counters for each field.
        #Initialise the list only once in the get_plot function
        self.participant.vars['counters'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
        return aoiVisualization

        
    
    

class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        
        # make the first one
        Game.create(group=group, iteration=group.iteration)


class Play(Page):
    form_model = 'player'
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)
    
    @staticmethod
    #Shall player x see the screen or not? => only player 2, 4, ... can see Biofeedback in cond 1 and 2
    #This functionnchecks if if of player is even and gets to receive biofeedback (No mathematicla operations in .html file possible)
    def vars_for_template(self):
        is_uneven = self.id_in_group % 2 == 1
        return {'is_uneven': is_uneven}



class Results(Page):
    pass

class Anleitung (Page): 
    @staticmethod
    def is_displayed(player:Player): 
        return player.round_number == 1;  


page_sequence = [Anleitung, WaitToStart, Play, Results]




def getAOI_Visualization():
    
    fig = go.Figure()


    # Set axes properties
    fig.update_xaxes(range=[0, 4.5])
    fig.update_yaxes(range=[0, 3.5])
    config = {'staticPlot': True}

    fig.update_layout(
    autosize = True,
    transition = {'duration': 1000, 'easing': 'cubic-in-out', 'ordering': 'layout first'},
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    xaxis = dict(
        showgrid = False,
        zeroline = False,
        showticklabels = False,
        showline = False
    ),
    yaxis = dict(
        showgrid = False,
        zeroline = False,
        showticklabels = False,
        showline = False
    )
    )

    # Add shapes
    #Left BG-Panel
    fig.add_shape(type="rect",
        x0=0, y0=0, x1=4.5, y1=3.5,
        line=dict(color="LightGrey"),
        fillcolor="White",
    )
    #Middle Panel in Left BG-Panel
    fig.add_shape(type="rect",
        x0=0.3, y0=1.45, x1=4.2, y1=3,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    
    #Payout matrix (4 individual fields plus left and top panelswith annotations)
    #Payoutmatrix Left Annotation Panel
    fig.add_shape(type="rect",
        x0=0.8, y0=1.75, x1=1.2, y1=2.55,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    #Payoutmatrix Top Annotation Panel
    fig.add_shape(type="rect",
        x0=0.8, y0=2.6, x1=3.7, y1=2.8,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    #Payoutmatrix Bottom-Left
    fig.add_shape(type="rect",
        x0=1.3, y0=1.75, x1=2.5, y1=2.1,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    #Payoutmatrix Bottom-Right
    fig.add_shape(type="rect",
        x0=2.6, y0=1.75, x1=3.7, y1=2.1,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    
    #Payoutmatrix Top-Left
    fig.add_shape(type="rect",
        x0=1.3, y0=2.2, x1=2.5, y1=2.55,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    #Payoutmatrix Top-Right
    fig.add_shape(type="rect",
        x0=2.6, y0=2.2, x1=3.7, y1=2.55,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    
    
    #Left Button in Left BG-Panel
    fig.add_shape(type="rect",
        x0=1, y0=0.5, x1=1.8, y1=0.9,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    #Right Button in Left BG-Panel
    fig.add_shape(type="rect",
        x0=2.4, y0=0.5, x1=3.2, y1=0.9,
        line=dict(color="RoyalBlue"),
        fillcolor="LightGrey",
    )
    fig.add_annotation(
        text = "Option A",
        x = 1.4,
        y = 0.7,
        font = dict(
            size = 14,
            color = "black"
        ),
        showarrow = False
        )

    fig.add_annotation(
        text = "Option B",
        x = 2.8,
        y = 0.7,
        font = dict(
            size = 14,
            color = "black"
        ),
        showarrow = False
        )
    fig.update_shapes(dict(xref='x', yref='y'))
    
    return fig

def updateAOI_Visualization (self,trackedAOI):

    fig = self.participant.vars["graph"]
    
    
    
    """
    fig.layout.shapes[0] ist das linke Hintergrund-Panel
    fig.layout.shapes[1] ist das mittlere Panel im linken Hintergrund-Panel

    fig.layout.shapes[4] ist das untere linke Feld der Auszahlungsmatrix
    fig.layout.shapes[5] ist das untere rechte Feld der Auszahlungsmatrix
    fig.layout.shapes[6] ist das obere linke Feld der Auszahlungsmatrix
    fig.layout.shapes[7] ist das obere rechte Feld der Auszahlungsmatrix
    
    fig.layout.shapes[8] ist der linke Button im linken Hintergrund-Panel
    fig.layout.shapes[9] ist der rechte Button im linken Hintergrund-Panel
    """
    
    switcher = {
    'Feld unten rechts': 5,
    'Feld mitte mitte' : 6,
    'Feld mitte rechts' : 7,
    'Feld unten mitte' : 4,
    'Feld oben rechts': 3,
    'Feld oben mitte' : 3,
    'Feld mitte links': 2,
    'Feld unten links' : 2,
    'Feld oben links' : 3,
    'Button cooperate' : 8,
    'Button defect' : 9,
    }
    aoiInput = switcher.get(trackedAOI, True) # Zwei

    if aoiInput == True:
        fig.update_shapes(dict(xref='x', yref='y'))
        return
    #Get preprocessed Data from AOI Tracker
    
    #Change the line color and width of the selected field
    fig.layout.shapes[aoiInput].line.color = "yellow"
    fig.layout.shapes[aoiInput].line.width = 3.5
    #Use the existing counter to keep track of the fading time
    #Reset the counter to zero if the field is marked again
    self.participant.vars['counters'][aoiInput] = 0 
    #Fade the line color and width of the selected field
    fade_line_color(self, fig, aoiInput)
    fig.update_shapes(dict(xref='x', yref='y'))
    #Fade the other fields that are not marked
    for i in range(1, 10):
        if i != aoiInput and self.participant.vars['counters'][i] > 0:
            fade_line_color(self, fig, i)

#A function to fade the line color and width of a shape
def fade_line_color(self, fig, i):
    
    speed = 10 #the lower the less method callsit takesto fade the marking ofthe panel
    #Convert hex color strings to RGB tuples
    color1 = hex_to_rgb("#FFFF00") #yellow
    color2 = hex_to_rgb("#3900B0") #original border color
    #Find the intermediate color at counter/duration fraction
    new_color = find_intermediate_color(color1, color2, self.participant.vars['counters'][i]/speed)
    new_color = (min(255, max(0, new_color[0])), min(255, max(0, new_color[1])), min(255, max(0, new_color[2])))
    new_width = max(1, 5 - (5 - 1) * self.participant.vars['counters'][i] / speed)
    #Update the line color and width of the shape
    fig.layout.shapes[i].line.color = f"rgb{new_color}" 
    #convert back to hex string
    fig.layout.shapes[i].line.width = new_width
    #Increase the counter by one
    self.participant.vars['counters'][i] += 1


    """
    #Dieser Code kann verwendet werden, um die Farbe der Bereiche in der AOI-Visualisierung farblich entsprechend einer Heatmap zu verändern,
    #je nachdem, wie oft eine Person ein bestimmtes Feld angesehen hat.
    
    counters = self.participant.vars["counters"]


    #Erhöhen Sie den Zähler für das ausgewählte Feld um eins
    
    counters[aoiInput] += 1

    #Verwenden Sie eine Farbskala, um den Zählerwert einer Farbe zuzuordnen
    colorscale = plotly.colors.n_colors(plotly.colors.hex_to_rgb("#D3D3D3"), plotly.colors.hex_to_rgb("#FF0000"), n_colors=15)


    #Aktualisieren Sie die Farbe jedes Feldes in einer Schleife [index nur 2-8, da 1 Der Hintergrund des Panels ist]
    for i in range(2, 10):
        #Begrenzen Sie den Zählerwert auf die Länge der Farbskala
        color_index = min(counters[i], len(colorscale) - 1)
        #Wählen Sie die entsprechende Farbe aus der Farbskala aus
        color = colorscale[color_index]
        #Weisen Sie die Farbe dem Feld zu
        fig.layout.shapes[i].fillcolor = f"rgb{color}"

    """
    
    
    fig.update_shapes(dict(xref='x', yref='y'))
    
# A function that receives the dictionary with the position data and the x and y data of the gaze
def mappingGazeData (data, gaze_df):
    mapping_data = data["tableData"]
    # Create a dictionary to store the number of gaze points for each field
    gaze_count = {}
    
    # Go through all rows in the DataFrame
    for index, row in gaze_df.iterrows():
        # Convert the gaze_x and gaze_y data into pixel coordinates
        pixel_x = row["gaze_x"] * data["screenWidth"]
        pixel_y = row["gaze_y"] * data["screenHeight"]
        # Go through all fields in the dictionary
        for field_name, field_data in mapping_data.items():
            # Check if the pixel coordinates are within the rectangle boundaries of the field
            if field_data["rectLeft"] <= pixel_x <= field_data["rectRight"] and field_data["rectTop"] <= pixel_y <= field_data["rectBottom"]:
                # If yes, increase the counter for the field by one
                gaze_count[field_name] = gaze_count.get(field_name, 0) + 1
                # End the inner loop as the field was found
                break

    # Calculate the total number of gaze points
    total_gaze = sum(gaze_count.values())

    # Create a list to store the percentage breakdown for each field
    gaze_percentage = []
    if (total_gaze != 0):

        # Go through all fields in the dictionary
        for field_name, field_data in mapping_data.items():
            # Calculate the percentage of gaze points for the field
            percentage = round(gaze_count.get(field_name, 0) / total_gaze * 100, 2)
            # Add the field name and the percentage to the list
            gaze_percentage.append(f"{field_name}: {percentage}%")

        # Find the field with the most gaze points
        max_gaze_field = max(gaze_count, key=gaze_count.get)

        #print(gaze_percentage)
        #print(max_gaze_field)

        # Return the field with the most gaze points
        return  max_gaze_field
    else:
        return 100 #no value between 0-10 otherwiseit would highlightone of the panels



        

def getGazeData(player):
    
    other = player.get_others_in_group()[0]
    #We need the maapingID to get the EYEtracking Data of the corresponding participant/opponent
    otherParticipantMappingID = other.participant.vars["mappingID"]

    #define the query to select the gaze data for the last second with the given eyetracker id and pupil validity
    currentTimeStamp = datetime.datetime.now()
    currentTimeStampStr = currentTimeStamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] #truncate the last 3 digits of microseconds
    
    query = """
    SELECT time_stamp, gaze_x, gaze_y   
    FROM public.eyedata40
    WHERE mappingID = %s
    AND left_gaze_point_validity = 1 AND right_gaze_point_validity = 1
    AND time_stamp::timestamp >= %s::timestamp - INTERVAL '2000 millisecond';
    """

    #execute the query and store the results in a pandas dataframe
    df = pd.read_sql(query, conn, params=(otherParticipantMappingID, currentTimeStampStr))
    
    
    


    return df

    