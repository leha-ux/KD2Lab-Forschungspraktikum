
from otree.api import *
import numpy as np
import random
from random import *
import datetime



c = cu
class Constants(BaseConstants):
    name_in_url = 'TestSzenario2'
    players_per_group = 2
    num_rounds = 1
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
        # Send a response only to the other players 
        #Test Game Case: Dont send Response
        """
        for p in other_players:
            id = p.id_in_group
            response[id] = True
        """

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
    comprehensioncheckNumber = models.BooleanField(
        choices=[
            [True, 'Bei Szenario2 gewinnt derjenige die Auktion, der zuerst bietet.'],
            [False, 'Bei Szenario2 teilen Sie immer den Gewinn mit Ihrem Mitspieler.'],
            [False, 'Bei Szenario2 entscheiden Sie, wie viel Ihr Mitspieler zur Auktion beitragen muss.'],
            [False, 'Alle Antworten sind richtig.']
        ],
        label='Welche der folgenden Aussagen ist richtig?',
        widget=widgets.RadioSelect
    )
    is_correct = models.BooleanField()

    
    
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
    #Shall player x see the screen or not? => only player 2, 4, ... can see Biofeedback in cond 1 and 2
    #This functionnchecks if if of player is even and gets to receive biofeedback (No mathematicla operations in .html file possible)
    def vars_for_template(self):
        is_even = self.id_in_group % 2 == 0
        return {'is_even': is_even}

    

    
    

    
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'
class Results(Page):
    form_model = 'player'
    @staticmethod 
    def vars_for_template(player): 
        # Berechnen Sie den Wert von player.bid_amount - player.item_value_actual 
        value = player.item_value_actual - player.bid_amount
        # Geben Sie die Variable als ein Wörterbuch zurück 
        return dict(value=value)

        
        
class Question(Page):
    form_model = 'player'
    form_fields = ['comprehensioncheckNumber']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        #Payoff nach den Testspielen zurücksetzen
        player.payoff = 0
        print(player.payoff)
        if player.comprehensioncheckNumber == True:
            player.is_correct = True
            
        else:
            player.is_correct = False
            

class richtigeAntwort(Page):
    @staticmethod
    def is_displayed(player:Player): 
        return player.is_correct == True

    @staticmethod
    def vars_for_template(player: Player):
            return dict(
            is_correct=player.is_correct,
            correct_answer=Constants.correct_answer
            )
            
class falscheAntwort(Page): 
    @staticmethod
    def is_displayed(player:Player):
        # Überprüfen Sie die Bedingungen, ob die Seite übersprungen werden soll
        return player.is_correct == False  

page_sequence = [Introduction,  BidWaitPage, Bid, Results, Question, richtigeAntwort, falscheAntwort]

