from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'Instruktionen'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass 

# PAGES
class Instruktionen_1(Page):
    pass 
class Instruktionen_2(Page): 
    pass
class Anleitung (Page): 
    pass 


page_sequence = [Instruktionen_1, Instruktionen_2, Anleitung]
