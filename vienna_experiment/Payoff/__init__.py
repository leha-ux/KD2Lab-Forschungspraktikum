from otree.api import *
import random
from settings import PARTICIPANT_FIELDS
from statistics import mean

doc = """
"""

class C(BaseConstants):
    NAME_IN_URL = 'Payoff'
    PLAYERS_PER_GROUP = None
    INSTRUCTIONS_TEMPLATE = 'experiment/payoff.html'
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    None


class Group(BaseGroup):
    None 

class Player(BasePlayer):
    ergebnis = models.CurrencyField()
    gesamt = models.CurrencyField()

# FUNCTIONS    
class calculation(Page): 
    None

# PAGES
class payment(Page):
    def vars_for_template(player:Player):
        
        if (player.participant.payoff_plus_participation_fee() < 0): 
            player.ergebnis = 0 
            player.gesamt = player.ergebnis + 5
        else: 
            player.ergebnis = (player.participant.payoff_plus_participation_fee()/18)
            player.gesamt = player.ergebnis + 5
        return dict (
        )
    

page_sequence = [payment]

