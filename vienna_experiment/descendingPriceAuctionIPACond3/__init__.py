
from otree.api import *
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import psycopg2
import numpy as np
import random
from random import *
import datetime

#connection = "postgres://postgres:password@localhost:5432/riro2023"
#connect to Timescale database using the psycopg2 connect function
#conn = psycopg2.connect(connection)
#conn.autocommit = True

c = cu
class Constants(BaseConstants):
    name_in_url = 'cSzenario2'
    players_per_group = 2
    num_rounds = 3
    estimate_error_margin = cu(1)
    style_background_color = '#F0F0F0'
    style_text_color = '#1F297E'
    min_allowable_bid = 0
    max_allowable_bid = 10
    #bid_decrement has to be adjusted in Bid.html
    bid_decrement = 0.1
    timer_mode = 2
    animation_color = '#BAA382'
    display_opponents_results = True
    correct_answer = True
def creating_session(subsession):
    session = subsession.session
    
    
    for p in subsession.get_players():
        import random
    
        item_value = random.uniform(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )
        p.item_value_actual = round(item_value, 2)
        p.number_of_opponents = Constants.players_per_group - 1
class Subsession(BaseSubsession):
    pass
def set_winner(group):
    # import random
    
    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    
    players_with_highest_bid = [
        p for p in players if p.bid_amount == group.highest_bid
    ]
    
    # set winner to be random if nobody clicks bid
    # if timeout_happened = True,
    #    players_with_highest_bid.random().is_winner = True  
    
    # No player bids, winner set randomly
    # if (group.highest_bid == 0):
    #    random_winner = random.randint(0,2)
    #    players[random_winner].is_winner = True
    #    players[random_winner].is_timeout_winner = True
    
    # Same bid from two players 
    if (len(players_with_highest_bid) > 1):
        # if tied, payout divided between winners
        for p in players_with_highest_bid:
            p.is_tied = True;
            p.number_of_players_tied = len(players_with_highest_bid)
    
    # No tie, only one winner  
    else:
        players_with_highest_bid[0].is_winner = True
    
    for p in players:
        set_payoff(p)
    
    for p in players:
        p.total_earnings= sum([round.payoff for round in p.in_all_rounds()]) 
def bid_waiting(group):
    pass
class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    total_earnings = models.CurrencyField()
    num_messages = models.IntegerField()
    game_finished = models.BooleanField(initial=False)
def set_payoff(player):
    # Submits highest bid
    # if player.is_winner and not player.is_timeout_winner:
    if player.is_winner:
        player.payoff = player.item_value_actual - player.bid_amount
    
    # No bids and player is randomly chosen as winner
    # elif player.is_winner and player.is_timeout_winner:  
        # player.payoff = player.item_value_actual
    
    # Players submit tied bids
    elif player.is_tied:
        player.payoff = (player.item_value_actual - player.bid_amount)/ player.number_of_players_tied
    
    else:
        player.payoff = 0
def live_endBid(player, data):
    group = player.group
    #This method sends a response to all players, and JS code changes bid value for other players 
    #    my_id = player.id_in_group
    #    response = dict(bidder_id=my_id)
    #    return {0: response}
    other_players = player.get_others_in_group()
    response = {}

    if 'bidSubmit' in data:
        # Send a response only to the other players =
        for p in other_players:
            id = p.id_in_group
            response[id] = True
            
    if 'graph' in data:
        #IMPLEMENT DATENBANK ABFRAGE 
        value = 1
        #value = getIPA(player)
        value = randint(0,7)
        return {0: dict(graph=updatePUPIL_Visualization(player, value).to_json())}
            
    
    
    return response
def get_countdown_timer(player):
    pass
def otherPlayersValues(player):
    group = player.group
    playerList = player.get_others_in_group()
    valueList = []
    
    for player in playerList: 
        valueList.append(player.item_value_actual)
    
    return valueList
def other_player(player):
    group = player.group
    return player.get_others_in_group()[0]




class Player(BasePlayer):
    item_value = models.CurrencyField()
    bid_amount = models.CurrencyField(label='Bid amount')
    is_winner = models.BooleanField(initial=False)
    is_tied = models.BooleanField(initial=False)
    number_of_players_tied = models.IntegerField()
    item_value_actual = models.CurrencyField()
    total_earnings = models.CurrencyField()
    number_of_opponents = models.IntegerField()
    is_timeout_winner = models.BooleanField(initial=False)
    
    
    #Create PupilDilation Visualization for each Player 
    def get_plot(self): # 
        fig= createplot()
        self.participant.vars["graph"] = fig
        return fig.to_json() # Speichern Sie die Figur als JSON-String
    
    
class Introduction(Page):
    form_model = 'player'
class BidWaitPage(WaitPage):
    pass
class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']
    live_method = 'live_endBid'
    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            player_id = player.id_in_group,
            others_values = otherPlayersValues(player),
            display_opponents_results = Constants.display_opponents_results
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.bid_amount = 0
    @staticmethod
    def get_timeout_seconds(player):
        bid_seconds = (Constants.max_allowable_bid / Constants.bid_decrement) + 4
        return bid_seconds
    
    @staticmethod
    #Shall player x see the screen or not? => only player 1, 3, 
    #This function checks if if of player is uneven and gets to receive biofeedback (No mathematicla operations in .html file possible)
    def vars_for_template(self):
        is_uneven = self.id_in_group % 2 == 1
        return {'is_uneven': is_uneven}

    

    
    

    
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'
class Results(Page):
    form_model = 'player'
class Anleitung(Page): 
     @staticmethod
     def is_displayed(player:Player): 
        return player.round_number == 1; 
 
          
page_sequence = [Anleitung, BidWaitPage, Bid, ResultsWaitPage, Results]


def createplot():
        
    aoiInput = randint(0,7)#Get preprocessed Data from AOI Tracker
    plot_bgcolor = "#f5f5f5"
    quadrant_colors = [plot_bgcolor, "#f00", "#f66", "#ff6", "#6f6", "#afa"] 
    quadrant_text = ["", "5-6", "4-5", "3-4", "2-3","1-2",  "0-1" ]
    n_quadrants = len(quadrant_colors) - 1

        #Adjust this passage according to the data that is used - Specify min/max values accordingly
        #The current value can be part of the function get_plot(self, current_value) for dynamic adjustement 
        #get_plot() gets triggered when bid.html ins rendered
    current_value = aoiInput
    min_value = 0
    max_value = 6
        
        
    hand_length = np.sqrt(2) / 4
    hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
                ),
            ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0,t=10,l=10,r=10),
            width=350,
            height=350,
            paper_bgcolor=plot_bgcolor,
            annotations=[
                go.layout.Annotation(
                    #text=f"<b>Stresslevel des Gegenspielers</b><br>{current_value} units",
                    text=f"<b>Erregung des Gegenspielers</b><br>IPA: {current_value:.1f}",
                    x=0.5, xanchor="center", xref="paper",
                    y=0.25, yanchor="top", yref="paper",
                    showarrow=False,
                    )
                ],
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.48, x1=0.52,
                    y0=0.48, y1=0.52,
                    fillcolor="#333",
                    line_color="#333",
                    ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="#333", width=4)
                    )
                ]
            )
        )
    return fig


def updatePUPIL_Visualization(player, value):
    
    aoiInput = value#Get preprocessed Data from AOI Tracker
    plot_bgcolor = "#f5f5f5"
    quadrant_colors = [plot_bgcolor, "#f00", "#f66", "#ff6", "#6f6", "#afa"] 
    quadrant_text = ["", "5-6", "4-5", "3-4", "2-3","1-2",  "0-1" ]
    n_quadrants = len(quadrant_colors) - 1

        #Adjust this passage according to the data that is used - Specify min/max values accordingly
        #The current value can be part of the function get_plot(self, current_value) for dynamic adjustement 
        #get_plot() gets triggered when bid.html ins rendered
    current_value = aoiInput
    min_value = 0
    max_value = 6
        
        
    hand_length = np.sqrt(2) / 4
    hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
                ),
            ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0,t=10,l=10,r=10),
            width=350,
            height=350,
            paper_bgcolor=plot_bgcolor,
            annotations=[
                go.layout.Annotation(
                    #text=f"<b>Stresslevel des Gegenspielers</b><br>{current_value} units",
                    text=f"<b>Erregung des Gegenspielers</b><br>IPA: {current_value:.1f}",
                    x=0.5, xanchor="center", xref="paper",
                    y=0.25, yanchor="top", yref="paper",
                    showarrow=False,
                    )
                ],
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.48, x1=0.52,
                    y0=0.48, y1=0.52,
                    fillcolor="#333",
                    line_color="#333",
                    ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="#333", width=4)
                    )
                ]
            )
        )
    return fig




def getIPA(player):


    
    #define the query to select the gaze data for the last second with the given eyetracker id and pupil validity

    other = player.get_others_in_group()[0]
    #We need the maapingID to get the EYEtracking Data of the corresponding participant/opponent
    otherParticipantMappingID = other.participant.vars["mappingID"]
    
    #define the query to select the gaze data for the last second with the given eyetracker id and pupil validity
    currentTimeStamp = datetime.datetime.now()
    currentTimeStampStr = currentTimeStamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] #truncate the last 3 digits of microseconds

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!system_time_stamp has to be chaned back to gyze_y after correction
    query = """
    SELECT time_stamp, ipa_left, ipa_right   
    FROM public.eyedata40
    WHERE mappingID = %s
    AND left_pupil_validity = 1 AND right_pupil_validity = 1
    AND time_stamp::timestamp >= %s::timestamp - INTERVAL '2000 millisecond';
    """

    #execute the query and store the results in a pandas dataframe
    df = pd.read_sql(query, conn, params=(otherParticipantMappingID, currentTimeStampStr))
 
    #commit changes to the database
    conn.commit()

    #check if the dataframe is empty
    if df.empty:
        #set ipa_leftright_avg to False
        ipa_leftright_avg = False
    else:
        
        #calculate the mean of ipa_left and ipa_right columns
        ipa_left_mean = df["ipa_left"].mean()
        ipa_right_mean = df["ipa_right"].mean()

        #calculate the average of the two means
        ipa_leftright_avg = (ipa_left_mean + ipa_right_mean) / 2
        print(ipa_leftright_avg)

    return ipa_leftright_avg