
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
        import random
        value = (random.random(), random.random())
        #value = getPupil(player)
        return {0: dict(graph=updatePUPIL_Visualization(player, value[0], value[1]))}
    
    
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
        self.participant.vars["graph"] = {'left': 0.5, 'right': 0.5} 
        return self.participant.vars["graph"]  # Speichern Sie die Figur als JSON-String
    
    
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



def updatePUPIL_Visualization(player, leftValue, rightValue):
    return {'left': leftValue, 'right': rightValue} 


def getPupil(player):
    #define the query to select the gaze data for the last second with the given eyetracker id and pupil validity

    other = player.get_others_in_group()[0]
    #We need the maapingID to get the EYEtracking Data of the corresponding participant/opponent
    otherParticipantMappingID = other.participant.vars["mappingID"]
    
    #define the query to select the gaze data for the last second with the given eyetracker id and pupil validity
    currentTimeStamp = datetime.datetime.now()
    currentTimeStampStr = currentTimeStamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] #truncate the last 3 digits of microseconds

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!system_time_stamp has to be chaned back to gyze_y after correction
    query = """
    SELECT time_stamp, first_pupil_left, first_pupil_right, left_pupil_diameter, right_pupil_diameter 
    FROM public.eyedata40
    WHERE mappingID = %s
    AND left_pupil_validity = 1 AND right_pupil_validity = 1
    AND time_stamp::timestamp >= %s::timestamp - INTERVAL '3000 millisecond';
    """

    #execute the query and store the results in a pandas dataframe
    df = pd.read_sql(query, conn, params=(otherParticipantMappingID, currentTimeStampStr))
    
    #commit changes to the database
    conn.commit()

    #check if the dataframe is empty
    if df.empty:
        #set ipa_leftright_avg to False
        pupilDiameter = (0, 0)
    else:
        # Calculate the mean of left_pupil_diameter and right_pupil_diameter
        avg_left_pupil_diameter = df['left_pupil_diameter'].mean()
        avg_right_pupil_diameter = df['right_pupil_diameter'].mean()

        # Calculate the percentage change
        pct_change_left = min((avg_left_pupil_diameter / df['first_pupil_left'].iloc[0]), 1)
        pct_change_right = min((avg_right_pupil_diameter / df['first_pupil_right'].iloc[0]), 1)
        pupilDiameter = (pct_change_left, pct_change_right)
        #calculate the average of the two means
    return pupilDiameter


